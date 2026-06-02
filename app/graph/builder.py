from langgraph.graph import END, StateGraph

from app.agents.deep_agent import DeepAgent
from app.graph.state import DeepAgentState
from app.memory.store import MemoryStore


def build_deep_agent_graph(memory_store: MemoryStore | None = None):
    agent = DeepAgent(memory_store)
    graph = StateGraph(DeepAgentState)
    graph.add_node("load_memory", agent.load_memory)
    graph.add_node("plan", agent.plan)
    graph.add_node("select_tools", agent.select_tools)
    graph.add_node("execute_tools", agent.execute_tools)
    graph.add_node("synthesize", agent.synthesize)
    graph.add_node("save_memory", agent.save_memory)
    graph.set_entry_point("load_memory")
    graph.add_edge("load_memory", "plan")
    graph.add_edge("plan", "select_tools")
    graph.add_edge("select_tools", "execute_tools")
    graph.add_edge("execute_tools", "synthesize")
    graph.add_edge("synthesize", "save_memory")
    graph.add_edge("save_memory", END)
    return graph.compile()

