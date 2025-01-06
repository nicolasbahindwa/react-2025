# nodes/update_nodes.py
import uuid
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from trustcall import create_extractor
from models.llm_config import get_model
from models.schemas import Profile, ToDo
from prompts.system_prompts import TRUSTCALL_INSTRUCTION, CREATE_INSTRUCTIONS
from utils.tool_utils import Spy, extract_tool_info

def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update user profile information"""
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    namespace = ("profile", user_id)
    
    # Get existing memories
    existing_items = store.search(namespace)
    existing_memories = [
        (item.key, "Profile", item.value) for item in existing_items
    ] if existing_items else None
    
    # Prepare messages for extraction
    instruction = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    messages = [SystemMessage(content=instruction)] + state["messages"][:-1]
    
    # Create and invoke extractor
    model = get_model()
    profile_extractor = create_extractor(
        model,
        tools=[{
            "type": "function",
            "function": {
                "name": "Profile",
                "description": "Extracts user profile information",
                "parameters": Profile.model_json_schema(),
            },
        }],
        tool_choice="Profile",
    )
    
    result = profile_extractor.invoke({
        "messages": messages,
        "existing": existing_memories
    })
    
    # Save results
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(
            namespace,
            rmeta.get("json_doc_id", str(uuid.uuid4())),
            r.model_dump(mode="json"),
        )
    
    return {
        "messages": [{
            "role": "tool",
            "content": "updated profile",
            "tool_call_id": state["messages"][-1].tool_calls[0]["id"],
        }]
    }

def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update todo list items"""
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    namespace = ("todo", user_id)
    
    # Similar structure to update_profile but for todos
    existing_items = store.search(namespace)
    existing_memories = [
        (item.key, "ToDo", item.value) for item in existing_items
    ] if existing_items else None
    
    instruction = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    messages = [SystemMessage(content=instruction)] + state["messages"][:-1]
    
    spy = Spy()
    model = get_model()
    todo_extractor = create_extractor(
        model,
        tools=[{
            "type": "function",
            "function": {
                "name": "ToDo",
                "description": "Captures task information",
                "parameters": ToDo.model_json_schema(),
            },
        }],
        tool_choice="ToDo",
        enable_inserts=True,
    ).with_listeners(on_end=spy)
    
    result = todo_extractor.invoke({
        "messages": messages,
        "existing": existing_memories
    })
    
    # Save results and return update message
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(
            namespace,
            rmeta.get("json_doc_id", str(uuid.uuid4())),
            r.model_dump(mode="json"),
        )
    
    todo_update_msg = extract_tool_info(spy.called_tools, "ToDo")
    return {
        "messages": [{
            "role": "tool",
            "content": todo_update_msg,
            "tool_call_id": state["messages"][-1].tool_calls[0]["id"],
        }]
    }

def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Update system instructions"""
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    namespace = ("instructions", user_id)
    
    existing_memory = store.get(namespace, "user_instructions")
    
    system_msg = CREATE_INSTRUCTIONS.format(
        current_instructions=existing_memory.value if existing_memory else None
    )
    
    model = get_model()
    new_memory = model.invoke(
        [SystemMessage(content=system_msg)]
        + state["messages"][:-1]
        + [HumanMessage(content="Please update the instructions based on the conversation")]
    )
    
    store.put(namespace, "user_instructions", {"memory": new_memory.content})
    
    return {
        "messages": [{
            "role": "tool",
            "content": "updated instructions",
            "tool_call_id": state["messages"][-1].tool_calls[0]["id"],
        }]
    }