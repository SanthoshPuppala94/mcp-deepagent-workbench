# Architecture

## Business Problem

Many GenAI demos stop at a single chatbot. This project demonstrates a more
serious agent platform pattern: tool servers, graph orchestration, explicit
memory, and testable execution phases.

## Components

- **FastAPI** exposes `/run` for application clients.
- **FastMCP** exposes tools/resources for MCP-compatible clients.
- **LangGraph** orchestrates deep-agent phases.
- **LangChain tool adapters** wrap the same functions as `StructuredTool`
  objects.
- **SQLite memory** stores user profile memory and task history.
- **Knowledge resources** provide local MCP resources for agent design notes.

## Deep Agent Flow

1. Load long-term user memory from SQLite.
2. Decompose the task into a plan.
3. Select tools based on task intent.
4. Execute knowledge search and risk assessment tools.
5. Synthesize a final answer with citations.
6. Persist useful memory and task result.

## Production Considerations

- Keep MCP tools narrow and auditable.
- Validate tool inputs and avoid broad filesystem/database access.
- Store memory intentionally and avoid sensitive data by default.
- Add approval gates before destructive or external actions.
- Test graph nodes independently and end to end.
- Separate API, MCP, tools, graph, and memory boundaries.

