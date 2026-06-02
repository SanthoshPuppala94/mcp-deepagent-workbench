import asyncio

from app.mcp_server.server import mcp


def test_mcp_tools_are_registered():
    async def run():
        tools = await mcp.list_tools()
        return {tool.name for tool in tools}

    tool_names = asyncio.run(run())
    assert {"search_agent_knowledge", "decompose_agent_task", "assess_agent_risks", "run_deep_agent"}.issubset(
        tool_names
    )


def test_mcp_resources_are_registered():
    async def run():
        resources = await mcp.list_resources()
        return {str(resource.uri) for resource in resources}

    resource_uris = asyncio.run(run())
    assert {
        "knowledge://mcp-design",
        "knowledge://deep-agent-patterns",
        "knowledge://memory-design",
    }.issubset(resource_uris)

