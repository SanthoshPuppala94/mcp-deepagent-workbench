from app.tools.analysis_tools import assess_risks, decompose_task
from app.tools.knowledge_tools import search_knowledge


def build_langchain_tools():
    """Return LangChain StructuredTool adapters when LangChain is installed."""
    try:
        from langchain_core.tools import StructuredTool
    except ImportError as exc:
        raise RuntimeError("Install langchain-core to build LangChain tool adapters.") from exc

    return [
        StructuredTool.from_function(
            func=search_knowledge,
            name="search_agent_knowledge",
            description="Search local deep-agent knowledge notes.",
        ),
        StructuredTool.from_function(
            func=decompose_task,
            name="decompose_agent_task",
            description="Break a deep-agent task into steps.",
        ),
        StructuredTool.from_function(
            func=assess_risks,
            name="assess_agent_risks",
            description="Assess production risks for agentic AI systems.",
        ),
    ]

