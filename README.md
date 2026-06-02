# MCP DeepAgent Workbench

Production-style GenAI portfolio project focused on MCP servers, tools, deep
agent workflows, memory, LangChain tool adapters, and LangGraph orchestration.

## What It Demonstrates

- FastMCP server with decorated tools and resources
- LangGraph deep-agent workflow with explicit state transitions
- LangChain-compatible `StructuredTool` adapters
- Short-term graph state and long-term SQLite memory
- Tool selection, task decomposition, knowledge search, risk assessment
- FastAPI endpoint for running the agent
- pytest coverage for routing, memory, MCP registration, and graph execution

## Architecture

```text
FastAPI / MCP Client
        ↓
LangGraph DeepAgent
        ↓
Plan → Select Tools → Execute Tools → Synthesize → Save Memory
        ↓
Tools: search knowledge, decompose task, assess risks
        ↓
SQLite long-term memory + local knowledge resources
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run API

```powershell
uvicorn app.main:app --reload --port 8020
```

Example:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8020/run `
  -ContentType "application/json" `
  -Body '{"task":"Design a production MCP deep agent with memory and SQL safety"}'
```

## Run MCP Server

```powershell
python -m app.mcp_server
```

Decorated MCP tools:

- `search_agent_knowledge`
- `decompose_agent_task`
- `assess_agent_risks`
- `run_deep_agent`

Decorated MCP resources:

- `knowledge://mcp-design`
- `knowledge://deep-agent-patterns`
- `knowledge://memory-design`

## Run Tests

```powershell
pytest
```

## Interview Positioning

Say this project shows how to build a production-style tool-using deep agent:
MCP exposes governed tools/resources, LangGraph controls the agent lifecycle,
LangChain adapters make tools reusable in standard agent stacks, and SQLite
memory demonstrates persistent personalization without hiding state in prompts.

