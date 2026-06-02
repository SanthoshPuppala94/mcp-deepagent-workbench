from typing import Any

from mcp.server.fastmcp import FastMCP

from app.graph.builder import build_deep_agent_graph
from app.tools.analysis_tools import assess_risks, decompose_task
from app.tools.knowledge_tools import read_resource_file, search_knowledge


mcp = FastMCP(
    name="mcp-deepagent-workbench",
    instructions=(
        "Production-style MCP server exposing deep-agent tools, knowledge resources, "
        "risk analysis, and a LangGraph-backed agent run capability."
    ),
)


@mcp.tool()
def search_agent_knowledge(query: str, limit: int = 3) -> list[dict[str, str | int]]:
    """Search local deep-agent knowledge notes."""
    return search_knowledge(query, limit)


@mcp.tool()
def decompose_agent_task(task: str) -> list[str]:
    """Break an agentic AI task into execution steps."""
    return decompose_task(task)


@mcp.tool()
def assess_agent_risks(text: str) -> list[dict[str, str]]:
    """Assess production risks in agent, MCP, SQL, memory, and PII scenarios."""
    return assess_risks(text)


@mcp.tool()
def run_deep_agent(task: str, user_id: str = "demo-user") -> dict[str, Any]:
    """Run the LangGraph deep agent workflow."""
    graph = build_deep_agent_graph()
    result = graph.invoke({"task": task, "user_id": user_id})
    return {
        "answer": result["answer"],
        "plan": result.get("plan", []),
        "tools_used": result.get("selected_tools", []),
        "citations": result.get("citations", []),
    }


@mcp.resource("knowledge://mcp-design")
def mcp_design_notes() -> str:
    """MCP design notes for production tool servers."""
    return read_resource_file("mcp_design.md")


@mcp.resource("knowledge://deep-agent-patterns")
def deep_agent_patterns() -> str:
    """Deep-agent workflow patterns."""
    return read_resource_file("deep_agent_patterns.md")


@mcp.resource("knowledge://memory-design")
def memory_design() -> str:
    """Memory design notes for short-term and long-term agent memory."""
    return read_resource_file("memory_design.md")


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()

