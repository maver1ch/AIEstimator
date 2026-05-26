from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedQuantityItem(BaseModel):
    """
    Items extracted by the LLM from schedules or drawings.
    This is PROBABILISTIC data that must be passed to the deterministic engine.
    """
    item_type: str = Field(..., description="E.g., Door, Paint, Gypsum Board")
    description: str = Field(..., description="Description of the item")
    raw_quantity: Optional[float] = Field(None, description="Extracted numerical quantity")
    unit: str = Field(..., description="Unit of measurement: EA, LF, SF, etc.")
    source_citation: str = Field(..., description="Must cite exact Sheet ID or Spec Section")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence of extraction")

class DocumentUploadResponse(BaseModel):
    filename: str
    status: str
    message: str
    document_id: int
