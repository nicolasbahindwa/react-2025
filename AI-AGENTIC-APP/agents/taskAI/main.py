# main.py
from config.settings import Configuration, ModelConfig
from graph.graph_builder import create_graph

# Create and use the graph
graph = create_graph()

# Use with configuration
config = Configuration()
response = graph.invoke({
    "messages": [...],
    "configurable": {
        "user_id": "user-123",
        "model_name": "fireworks"
    }
})