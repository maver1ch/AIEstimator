from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import tempfile
import os
from backend.api.deps import get_db, get_parser_service

router = APIRouter()

@router.post("/upload/")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = "spec", # 'plan' or 'spec'
    db: Session = Depends(get_db),
    parser_service: DoclingParserService = Depends(get_parser_service)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    # Save uploaded file to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        with temp_file as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Parse Document using Docling
        parsed_result = parser_service.parse_pdf(temp_file.name)
        
        # 2. Store to Database (simplified for MVP)
        # In a full implementation, we'd chunk `parsed_result['markdown']` 
        # and create embeddings before saving.
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": "Document parsed successfully",
            "markdown_preview": parsed_result["markdown"][:500] + "..." # Just for preview
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
