from typing import Generator
from backend.core.db import SessionLocal
from backend.services.docling_parser import DoclingParserService
from backend.services.ai_reasoning.agent import EstimatorAgentService

# Keep singletons for heavy services
_docling_parser_service = DoclingParserService()
_estimator_agent_service = EstimatorAgentService()

def get_db() -> Generator:
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_parser_service() -> DoclingParserService:
    """Dependency for getting the Docling Parser Service."""
    return _docling_parser_service

def get_agent_service() -> EstimatorAgentService:
    """Dependency for getting the AI Agent Service."""
    return _estimator_agent_service
