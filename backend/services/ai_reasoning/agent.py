from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from backend.core.config import settings
from backend.services.ai_reasoning.agent_tools import (
    search_specifications, 
    lookup_material_price, 
    calculate_takeoff_totals, 
    apply_equipment_rules
)
import logging

logger = logging.getLogger(__name__)

class EstimatorAgentService:
    def __init__(self):
        # Using a model that supports robust tool calling
        self.llm = ChatAnthropic(
            model_name=settings.MODEL_NAME,
            temperature=0, # Temperature 0 for deterministic tool calling
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )
        
        self.tools = [
            search_specifications,
            lookup_material_price,
            calculate_takeoff_totals,
            apply_equipment_rules
        ]
        
        # Create the prompt for the tool-calling agent
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are a highly disciplined Senior Construction Estimator AI. "
             "Your role is to assist human estimators with scope analysis, RFI drafting, and takeoff. "
             "CORE PRINCIPLE: You must NEVER fabricate data, numbers, or prices. "
             "Always use your provided tools to search specifications, lookup prices, or perform math. "
             "If asked to sum up counts, use calculate_takeoff_totals. "
             "If asked for prices, use lookup_material_price. "
             "If you don't know something or a tool returns no data, state clearly that information is missing."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Construct the tool calling agent
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        
        # Create an agent executor by passing in the agent and tools
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def process_query(self, user_input: str) -> str:
        """
        Runs the estimator agent with the user's natural language query.
        """
        logger.info(f"Running Estimator Agent for query: {user_input}")
        try:
            response = self.agent_executor.invoke({"input": user_input})
            return response["output"]
        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            return f"An error occurred while processing your request: {str(e)}"
