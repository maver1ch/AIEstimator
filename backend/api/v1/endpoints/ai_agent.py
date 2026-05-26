from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.ai_reasoning.agent import EstimatorAgentService

router = APIRouter()
agent_service = EstimatorAgentService()

class AgentRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    response: str

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(request: AgentRequest):
    """
    Endpoint for Natural-Language Estimator Controls.
    Users can ask the agent to perform estimating tasks, and it will use its tools.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        # Run the agent
        output = agent_service.process_query(request.query)
        return AgentResponse(response=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
