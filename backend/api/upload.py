from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import tempfile
import os
import logging
from backend.api.deps import get_db, get_parser_service
from backend.services.docling_parser import DoclingParserService
from backend.models.document import Document, DocumentChunk
from backend.core.config import settings

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = "spec", # 'plan' or 'spec'
    db: Session = Depends(get_db),
    parser_service: DoclingParserService = Depends(get_parser_service)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    try:
        # 1. Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        # 2. Parse using Docling
        # Docling is a highly advanced parser capable of understanding document layouts (e.g., multi-column text) 
        # and accurately extracting complex tables, which is critical for construction Takeoffs.
        logger.info(f"Parsing document: {file.filename}")
        parsed_data = parser_service.parse_pdf(temp_file_path)
        markdown_text = parsed_data["markdown"]
        
        # 3. Create Document Record & Extract Tables
        # We store the extracted tables directly in the metadata JSON so they can be readily
        # served to the Frontend (Takeoff Tab) without needing to re-parse the PDF.
        tables_json = []
        if "tables" in parsed_data:
            for df in parsed_data["tables"]:
                tables_json.append(df.to_dict(orient="records"))
                
        db_doc = Document(
            filename=file.filename, 
            file_type=doc_type,
            metadata_json={"extracted_tables": tables_json}
        )
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)

        # 4. Chunking (Text Splitting)
        # We split the long markdown into smaller chunks (1000 chars) with a 200 char overlap.
        # Overlapping prevents cutting off important context (like a spec requirement split between two chunks).
        logger.info("Chunking document text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_text(markdown_text)

        # 5. Generate Vector Embeddings
        # We use OpenAI's Embedding model to convert the text chunks into 1536-dimensional float vectors.
        # This allows us to perform semantic search (understanding meaning, not just keyword matching).
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        embeddings = embeddings_model.embed_documents(chunks)

        # 6. Save Chunks to Vector Database (pgvector)
        # The chunks and their corresponding embeddings are stored in PostgreSQL using the pgvector extension.
        db_chunks = []
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            db_chunk = DocumentChunk(
                document_id=db_doc.id,
                page_number=1, # Simplified for MVP
                content=chunk_text,
                content_type="text",
                embedding=embedding
            )
            db_chunks.append(db_chunk)
            
        db.add_all(db_chunks)
        db.commit()

        os.unlink(temp_file_path)
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"Successfully parsed and embedded {len(chunks)} chunks.",
            "document_id": db_doc.id,
            "tables_extracted": len(tables_json)
        }
        
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@router.get("/documents/")
def get_documents(db: Session = Depends(get_db)):
    """Fetch all parsed documents and their extracted tables (if any)."""
    docs = db.query(Document).order_by(Document.id.desc()).all()
    return docs

