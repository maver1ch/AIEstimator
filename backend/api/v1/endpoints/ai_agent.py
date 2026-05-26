from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.services.ai_reasoning.agent import EstimatorAgentService
from backend.api.deps import get_agent_service

router = APIRouter()

class AgentRequest(BaseModel):
    query: str
    project_id: str = "default_project"

class AgentResponse(BaseModel):
    response: str

@router.post("/chat", response_model=AgentResponse)
async def chat_with_agent(
    request: AgentRequest,
    agent_service: EstimatorAgentService = Depends(get_agent_service)
):
    """
    Endpoint for Natural-Language Estimator Controls.
    Users can ask the agent to perform estimating tasks, and it will use its tools.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        # Run the agent
        output = agent_service.process_query(request.query, project_id=request.project_id)
        return AgentResponse(response=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
