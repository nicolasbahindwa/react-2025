#nodes/task_maistro.py
from langchain_core.messages import SystemMessage
from config.settings import Configuration  # Added this import
from models.llm_config import get_model
from models.schemas import UpdateMemory
from prompts.system_prompts import MODEL_SYSTEM_MESSAGE
from services.memory_service import MemoryService
from langgraph.graph import MessagesState  # Added this for type hint
from langchain_core.runnables import RunnableConfig  # Added this for type hint
from langgraph.store.base import BaseStore  # Added this for type hint

def task_mAIstro(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Main chatbot node for processing user input"""
    
    try:
        configurable = Configuration.from_runnable_config(config)
        memory_service = MemoryService(store, configurable.user_id)
        
        # Get all required memories
        user_profile = memory_service.get_profile()
        todo = memory_service.get_todos()
        instructions = memory_service.get_instructions()
        
        # Format system message
        system_msg = MODEL_SYSTEM_MESSAGE.format(
            user_profile=user_profile, 
            todo=todo, 
            instructions=instructions
        )
        
        # Get model response
        model = get_model()
        response = model.bind_tools([UpdateMemory]).invoke(
            [SystemMessage(content=system_msg)] + state["messages"]
        )
        
        return {"messages": [response]}

    except Exception as e:
        return {"messages": [{"role": "system", "content": f"Error: {str(e)}"}]}