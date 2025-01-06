# graph/graph_builder.py

from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.store.base import BaseStore

# Import configuration
from config.settings import Configuration, ModelConfig

# Import nodes
from nodes.task_maistro import task_mAIstro
from nodes.update_nodes import update_todos, update_profile, update_instructions

class GraphBuilder:
    """Builder class for the conversation graph"""
    
    @staticmethod
    def route_message(
        state: MessagesState,
        config: RunnableConfig,
        store: BaseStore
    ) -> Literal[END, "update_todos", "update_instructions", "update_profile"]:
        """Route messages to appropriate update nodes based on tool calls."""
        message = state["messages"][-1]
        
        if len(message.tool_calls) == 0:
            return END
            
        tool_call = message.tool_calls[0]
        update_type = tool_call["args"]["update_type"]
        
        if update_type == "user":
            return "update_profile"
        elif update_type == "todo":
            return "update_todos"
        elif update_type == "instructions":
            return "update_instructions"
        else:
            raise ValueError(f"Unknown update type: {update_type}")

    @classmethod
    def build(cls) -> StateGraph:
        """Build and return the compiled state graph."""
        # Initialize graph with configuration
        builder = StateGraph(MessagesState, config_schema=Configuration)
        
        # Add all nodes
        builder.add_node("task_mAIstro", task_mAIstro)
        builder.add_node("update_todos", update_todos)
        builder.add_node("update_profile", update_profile)
        builder.add_node("update_instructions", update_instructions)
        
        # Define the conversation flow
        builder.add_edge(START, "task_mAIstro")
        builder.add_conditional_edges(
            "task_mAIstro",
            cls.route_message,
            {
                "update_profile": "update_profile",
                "update_todos": "update_todos",
                "update_instructions": "update_instructions",
                END: END
            }
        )
        
        # Add return edges to main conversation node
        builder.add_edge("update_todos", "task_mAIstro")
        builder.add_edge("update_profile", "task_mAIstro")
        builder.add_edge("update_instructions", "task_mAIstro")
        
        return builder.compile()

def create_graph(store: BaseStore = None) -> StateGraph:
    """Factory function to create and configure the graph."""
    if store is None:
        from langgraph.store.memory import InMemoryStore
        store = InMemoryStore()
        
    return GraphBuilder.build()