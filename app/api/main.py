from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import get_settings
from app.graph.builder import build_deep_agent_graph
from app.memory.store import MemoryStore


class RunRequest(BaseModel):
    task: str = Field(..., min_length=1)
    user_id: str = "demo-user"


class RunResponse(BaseModel):
    answer: str
    plan: list[str]
    tools_used: list[str]
    citations: list[str] = []


settings = get_settings()
memory_store = MemoryStore(settings.database_path)
graph = build_deep_agent_graph(memory_store)
app = FastAPI(title=settings.app_name, version="0.1.0")


@app.post("/run", response_model=RunResponse)
def run_agent(request: RunRequest) -> RunResponse:
    result = graph.invoke({"task": request.task, "user_id": request.user_id})
    return RunResponse(
        answer=result["answer"],
        plan=result.get("plan", []),
        tools_used=result.get("selected_tools", []),
        citations=result.get("citations", []),
    )

