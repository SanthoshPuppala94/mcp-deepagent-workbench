import re


RISK_TERMS = {
    "secret": "Secrets must be loaded from environment or a vault, never hardcoded.",
    "sql": "SQL tools should enforce read-only access, validation, and audit logging.",
    "pii": "PII should be minimized, redacted, encrypted, and access controlled.",
    "mcp": "MCP tools should use least privilege and explicit schemas.",
    "agent": "Agent tool calls should be observable, constrained, and recoverable.",
}


def decompose_task(task: str) -> list[str]:
    task_lower = task.lower()
    steps = ["Clarify the objective and expected output"]
    if "mcp" in task_lower or "tool" in task_lower:
        steps.append("Identify MCP tools and resource boundaries")
    if "memory" in task_lower:
        steps.append("Load short-term and long-term memory")
    if "risk" in task_lower or "security" in task_lower:
        steps.append("Assess production risks and controls")
    steps.append("Synthesize findings into an actionable answer")
    return steps


def assess_risks(text: str) -> list[dict[str, str]]:
    lowered = text.lower()
    findings = []
    for term, guidance in RISK_TERMS.items():
        if re.search(rf"\b{re.escape(term)}\b", lowered):
            findings.append({"term": term, "guidance": guidance})
    return findings

