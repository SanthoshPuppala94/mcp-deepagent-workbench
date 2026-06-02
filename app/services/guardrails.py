GUARDRAIL_NOTE = (
    "Guardrail note: This response is grounded in local tools/resources where citations are provided. "
    "For production use, validate tool outputs, enforce policy checks, and require human approval for risky actions."
)


def requires_grounding(task: str) -> bool:
    grounded_terms = ("mcp", "memory", "langgraph", "langchain", "agent", "tool", "security", "risk")
    return any(term in task.lower() for term in grounded_terms)


def validate_grounding(task: str, citations: list[str]) -> tuple[bool, str]:
    if not requires_grounding(task):
        return True, ""
    if citations:
        return True, ""
    return (
        False,
        "I do not have grounded tool/resource evidence for this task. "
        "Run knowledge search or provide citations before using this answer.",
    )


def add_guardrail_note(answer: str) -> str:
    if GUARDRAIL_NOTE in answer:
        return answer
    return f"{answer}\n\n{GUARDRAIL_NOTE}"

