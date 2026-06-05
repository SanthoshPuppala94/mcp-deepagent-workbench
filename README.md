# 🤖 MCP DeepAgent Workbench

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://langchain.com)
[![MCP](https://img.shields.io/badge/FastMCP-8B5CF6?style=flat)](https://github.com/jlowin/fastmcp)
[![pytest](https://img.shields.io/badge/Tested_with-pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)](https://pytest.org)

> **Production-style deep-agent framework** — Demonstrates MCP tool governance, LangGraph state machine orchestration, LangChain tool adapters, and persistent SQLite memory with hallucination controls and evidence-limited fallbacks.

---

## What It Does

This workbench implements a **LangGraph deep-agent** that executes complex tasks through explicit, auditable state transitions. Tools are governed via a **FastMCP server** with typed schemas. Long-term memory persists in SQLite — no state hidden in prompts.

---

## Architecture

```
POST /run
    │
    ▼
LangGraph DeepAgent
    │
    ├── [Plan]           → Decompose the task into steps
    ├── [Select Tools]   → Choose relevant MCP tools
    ├── [Execute Tools]  → Run tools with evidence collection
    ├── [Synthesize]     → Build grounded, cited response
    └── [Save Memory]    → Persist to SQLite long-term store
    │
    ▼
FastMCP Server (stdio)
    ├── Tools:     search_agent_knowledge
    │              decompose_agent_task
    │              assess_agent_risks
    │              run_deep_agent
    └── Resources: knowledge://mcp-design
                   knowledge://deep-agent-patterns
                   knowledge://memory-design
    │
    ▼
LangChain StructuredTool adapters
(tools reusable in any LangChain agent stack)
```

---

## Key Design Decisions

- **Explicit state transitions** — Every agent step is a named LangGraph node with defined inputs/outputs; no hidden chain-of-thought magic
- **LangChain adapters** — MCP tools are wrapped as `StructuredTool` so they work in any LangChain agent without rewriting
- **FastMCP governance** — Tools and resources declared with typed schemas; compatible clients can discover and enumerate capabilities
- **SQLite memory** — Long-term preferences and task history stored explicitly in a database, not embedded in prompt context
- **Hallucination controls** — Grounded tasks require tool citations; if evidence is absent, the agent returns a fallback rather than inventing details
- **Risk guardrails** — Final responses include an explicit guardrail note for production-impacting actions

---

## Getting Started

### Prerequisites
- Python 3.11+

### Setup

```bash
git clone https://github.com/SanthoshPuppala94/mcp-deepagent-workbench
cd mcp-deepagent-workbench

python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

### Run the API

```bash
uvicorn app.main:app --reload --port 8020
```

### Run the MCP Server

```bash
python -m app.mcp_server
```

### Run Tests

```bash
pytest
```

---

## Example Usage

```bash
# Design a production agent
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8020/run `
  -ContentType "application/json" `
  -Body '{"task":"Design a production MCP deep agent with memory and SQL safety"}'

# Assess risks
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8020/run `
  -ContentType "application/json" `
  -Body '{"task":"Assess risks of deploying a tool-using agent in a regulated environment"}'
```

### API Contract

**Request**
```json
{ "task": "Design a production MCP deep agent with memory and SQL safety" }
```

**Response**
```json
{
  "result": "Based on knowledge://mcp-design and knowledge://memory-design...",
  "steps_taken": ["plan", "select_tools", "execute_tools", "synthesize"],
  "citations": ["knowledge://mcp-design", "knowledge://memory-design"],
  "guardrail_note": "Validate tool outputs before applying to production systems."
}
```

---

## Project Structure

```
mcp-deepagent-workbench/
├── app/
│   ├── main.py           # FastAPI app + /run endpoint
│   ├── agent.py          # LangGraph deep-agent graph definition
│   ├── mcp_server.py     # FastMCP tools and resources
│   ├── adapters.py       # LangChain StructuredTool wrappers
│   └── memory.py         # SQLite long-term memory
├── data/
│   └── knowledge/        # Local knowledge resources
├── tests/                # pytest suite (routing, memory, MCP, graph)
├── architecture.md       # Full architecture walkthrough
├── pyproject.toml
├── .env.example
└── requirements.txt
```

---

## Guardrails Summary

| Guardrail | Implementation |
|-----------|---------------|
| Evidence requirement | Grounded tasks must cite local tools/resources |
| Evidence fallback | Returns explicit fallback if no citations found |
| Production safety | Guardrail note included for risky actions |
| Schema governance | MCP tools declared with typed FastMCP schemas |
| Memory hygiene | All state written to SQLite, not hidden in prompt |
| Secret hygiene | Credentials via `.env`, never hardcoded |

---

## About

Portfolio project demonstrating production deep-agent patterns: MCP tool governance, LangGraph lifecycle management, LangChain adapter reusability, and SQLite-backed persistent memory — with hallucination controls at every layer.
