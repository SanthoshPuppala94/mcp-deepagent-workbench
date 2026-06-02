from typing import Any, TypedDict


class DeepAgentState(TypedDict, total=False):
    task: str
    user_id: str
    plan: list[str]
    selected_tools: list[str]
    observations: list[dict[str, Any]]
    answer: str
    citations: list[str]
    memory: dict[str, Any]

