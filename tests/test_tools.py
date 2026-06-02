from app.tools.analysis_tools import assess_risks, decompose_task
from app.tools.knowledge_tools import search_knowledge


def test_decompose_task_includes_mcp_and_memory_steps():
    steps = decompose_task("Design MCP deep agent with memory")
    assert any("MCP" in step for step in steps)
    assert any("memory" in step.lower() for step in steps)


def test_assess_risks_finds_sql_and_pii():
    findings = assess_risks("Agent with SQL access and PII memory")
    terms = {finding["term"] for finding in findings}
    assert {"sql", "pii", "agent"}.issubset(terms)


def test_search_knowledge_returns_sources():
    results = search_knowledge("MCP tools resources production")
    assert results
    assert results[0]["source"].endswith(".md")

