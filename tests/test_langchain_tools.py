import pytest

from app.services.langchain_tools import build_langchain_tools


def test_langchain_tool_adapters_are_buildable_when_dependency_exists():
    try:
        tools = build_langchain_tools()
    except RuntimeError:
        pytest.skip("langchain-core is not installed in this verification environment")
    assert {tool.name for tool in tools} == {
        "search_agent_knowledge",
        "decompose_agent_task",
        "assess_agent_risks",
    }

