from typing import List, Dict, Any
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

# --- TOOL 1: RAG RETRIEVAL ---
@tool
def search_specifications(project_id: str, query: str, spec_section: str = None) -> str:
    """
    Use this tool to search the construction specifications. 
    Use it when you need to verify material requirements, performance specs (like NRC/CAC), or find missing details.
    Do NOT guess technical details, always use this tool to find the exact text.
    """
    logger.info(f"[Project: {project_id}] LLM called search_specifications with query: {query}")
    from backend.core.db import SessionLocal
    from backend.models.document import DocumentChunk, Document
    from langchain_openai import OpenAIEmbeddings
    from backend.core.config import settings

    try:
        embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        query_embedding = embeddings_model.embed_query(query)
        
        db = SessionLocal()
        # Search for top 3 closest chunks (cosine distance)
        results = db.query(DocumentChunk).order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        ).limit(3).all()
        db.close()

        if not results:
            return "No specifications found in the database."

        context = "\n\n".join([f"[From Doc {r.document_id}]: {r.content}" for r in results])
        return context
    except Exception as e:
        logger.error(f"Error in search_specifications: {e}")
        return f"Error occurred while searching specifications: {str(e)}"

# --- TOOL 2: DATABASE LOOKUP ---
@tool
def lookup_material_price(project_id: str, material_id: str) -> Dict[str, Any]:
    """
    Use this tool to get the exact cost of a material from the company's proprietary pricing database.
    NEVER invent or guess prices. Always use this tool.
    """
    logger.info(f"[Project: {project_id}] LLM called lookup_material_price for {material_id}")
    # TODO: Connect to Relational DB to fetch pricing
    return {"material_id": material_id, "unit_price": 12.50, "unit": "SF", "currency": "USD"}

# --- TOOL 3: DETERMINISTIC ENGINE DELEGATION ---
@tool
def calculate_takeoff_totals(project_id: str, extracted_items: List[dict]) -> Dict[str, float]:
    """
    Use this tool when you have extracted a list of quantities (e.g. door counts) and need the sum.
    Pass the extracted raw list. DO NOT attempt to add the numbers yourself.
    This tool calls the deterministic python engine to guarantee accurate math.
    """
    logger.info(f"[Project: {project_id}] LLM delegated calculation to deterministic engine.")
    # Here we bridge the Probabilistic AI with the Deterministic Engine
    from backend.services.calculation.quantity_aggregator import QuantityAggregator
    from backend.schemas.document import ExtractedQuantityItem
    
    # Parse dicts into strictly typed Pydantic models
    validated_items = [ExtractedQuantityItem(**item) for item in extracted_items]
    
    # Delegate math to the safe engine
    return QuantityAggregator.aggregate_counts(validated_items)

# --- TOOL 4: EQUIPMENT RULES ---
@tool
def apply_equipment_rules(working_height_ft: float) -> List[str]:
    """
    Use this tool to determine what equipment is needed based on the working height.
    """
    logger.info(f"LLM checking equipment for height: {working_height_ft}")
    # Deterministic rule
    equipment = []
    if working_height_ft > 12.0:
        equipment.append("Scissor Lift")
    if working_height_ft > 40.0:
        equipment.append("Boom Lift")
    return equipment
