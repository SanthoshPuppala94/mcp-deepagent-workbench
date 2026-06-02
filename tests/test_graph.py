from app.graph.builder import build_deep_agent_graph
from app.memory.store import MemoryStore


def test_deep_agent_graph_runs_end_to_end(tmp_path):
    graph = build_deep_agent_graph(MemoryStore(tmp_path / "graph.db"))
    result = graph.invoke({"task": "Design MCP agent with memory and production risk controls", "user_id": "u1"})
    assert "DeepAgent response" in result["answer"]
    assert "search_knowledge" in result["selected_tools"]
    assert "assess_risks" in result["selected_tools"]
    assert result["citations"]

