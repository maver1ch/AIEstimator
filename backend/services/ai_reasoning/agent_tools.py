from typing import List, Dict, Any
from langchain_core.tools import tool
import logging

logger = logging.getLogger(__name__)

# --- TOOL 1: RAG RETRIEVAL ---
@tool
def search_specifications(query: str, spec_section: str = None) -> str:
    """
    Use this tool to search the construction specifications. 
    Use it when you need to verify material requirements, performance specs (like NRC/CAC), or find missing details.
    Do NOT guess technical details, always use this tool to find the exact text.
    """
    logger.info(f"LLM called search_specifications with query: {query}")
    # TODO: Connect to pgvector database to perform semantic search
    return "MOCK: Spec 09 51 13 (Acoustical Panel Ceilings) requires minimum NRC of 0.70 and CAC of 35."

# --- TOOL 2: DATABASE LOOKUP ---
@tool
def lookup_material_price(material_id: str) -> Dict[str, Any]:
    """
    Use this tool to get the exact cost of a material from the company's proprietary pricing database.
    NEVER invent or guess prices. Always use this tool.
    """
    logger.info(f"LLM called lookup_material_price for {material_id}")
    # TODO: Connect to Relational DB to fetch pricing
    return {"material_id": material_id, "unit_price": 12.50, "unit": "SF", "currency": "USD"}

# --- TOOL 3: DETERMINISTIC ENGINE DELEGATION ---
@tool
def calculate_takeoff_totals(extracted_items: List[dict]) -> Dict[str, float]:
    """
    Use this tool when you have extracted a list of quantities (e.g. door counts) and need the sum.
    Pass the extracted raw list. DO NOT attempt to add the numbers yourself.
    This tool calls the deterministic python engine to guarantee accurate math.
    """
    logger.info("LLM delegated calculation to deterministic engine.")
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
