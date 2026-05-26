import logging
import tempfile
import os
from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)

class DoclingParserService:
    def __init__(self):
        self.converter = DocumentConverter()

    def parse_pdf(self, file_path: str):
        """
        Parses a PDF using Docling and returns structured data.
        Docling returns a DoclingDocument object which we can iterate over to get text and tables.
        """
        logger.info(f"Starting Docling parse for {file_path}")
        try:
            result = self.converter.convert(file_path)
            doc = result.document
            
            # Export to markdown as a basic format for chunking
            markdown_text = doc.export_to_markdown()
            
            # TODO: We can extract tables natively if needed
            # tables = doc.tables
            
            return {
                "markdown": markdown_text,
                "raw_doc": doc
            }
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            raise e
