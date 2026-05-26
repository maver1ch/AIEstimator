from typing import List
from backend.schemas.document import ExtractedQuantityItem

class QuantityAggregator:
    """
    DETERMINISTIC ENGINE
    This class is strictly responsible for math and aggregation. 
    It takes probabilistic inputs from the LLM and performs guaranteed calculations.
    """
    
    @staticmethod
    def aggregate_counts(items: List[ExtractedQuantityItem]) -> dict:
        """
        Groups and sums schedule-count takeoffs deterministically.
        """
        totals = {}
        for item in items:
            if not item.raw_quantity:
                continue
                
            key = f"{item.item_type} - {item.description}"
            if key not in totals:
                totals[key] = {
                    "total_quantity": 0,
                    "unit": item.unit,
                    "sources": set()
                }
            
            totals[key]["total_quantity"] += item.raw_quantity
            totals[key]["sources"].add(item.source_citation)
            
        # Convert sets to lists for JSON serialization
        for k in totals:
            totals[k]["sources"] = list(totals[k]["sources"])
            
        return totals
