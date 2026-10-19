import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.llm_pick import pick_llm
from models.schema import AgentSchema

# ------------------------------------ AI Agent Code ---------------------------------------

def curated_ques(state: AgentSchema) -> AgentSchema:
    """
        Curate the user question so that it can be properly understandable to LLM
    
        Args:
            state (AgentSchema): State of the current node
    
        Returns:
            AgentSchema: Add the curated question to the schema
        """

    user_question = state.user_question # As we are using Pydantic object model we can access property with period(.)
    llm = pick_llm("low")

    response = llm.invoke(f"Curate the following question: {user_question}")
    state.curated_ques = response

    return state 
