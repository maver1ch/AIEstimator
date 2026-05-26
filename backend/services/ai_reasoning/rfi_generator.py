import logging
from typing import List
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from backend.schemas.rfi import RFIItem, RFIListResponse
from backend.core.config import settings

logger = logging.getLogger(__name__)

class RFIGeneratorService:
    """
    PROBABILISTIC ENGINE
    This class handles the LLM logic to detect scope gaps and generate RFIs.
    """
    def __init__(self):
        # We enforce structured outputs using `.with_structured_output`
        self.llm = ChatAnthropic(
            model_name=settings.MODEL_NAME, 
            temperature=0.1, 
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        ).with_structured_output(RFIListResponse)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Senior Construction Estimator. Your job is to read the provided document chunk (Plans or Specs) and identify any scope gaps, missing dimensions, or unspecified materials. If you find gaps, draft professional RFIs (Requests for Information). YOU MUST NEVER FABRICATE DATA. If you are unsure, flag it with low confidence. You MUST explicitly cite the section or sheet provided."),
            ("user", "Document context:\n{context}\n\nPlease generate a structured list of RFIs based ONLY on this context.")
        ])

    def generate_rfis_from_context(self, context_text: str) -> RFIListResponse:
        """
        Takes a chunk of document context (e.g., from RAG) and asks the LLM to generate RFIs.
        Returns guaranteed Pydantic structures.
        """
        logger.info("Sending context to LLM for RFI generation...")
        chain = self.prompt | self.llm
        try:
            result = chain.invoke({"context": context_text})
            return result
        except Exception as e:
            logger.error(f"Error generating RFIs: {str(e)}")
            raise e
