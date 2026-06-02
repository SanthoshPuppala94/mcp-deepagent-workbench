from app.graph.state import DeepAgentState
from app.memory.store import MemoryStore
from app.services.guardrails import add_guardrail_note, validate_grounding
from app.tools.analysis_tools import assess_risks, decompose_task
from app.tools.knowledge_tools import search_knowledge


class DeepAgent:
    """Deterministic deep-agent workflow for production-style local demos."""

    def __init__(self, memory_store: MemoryStore | None = None):
        self.memory_store = memory_store or MemoryStore()

    def load_memory(self, state: DeepAgentState) -> DeepAgentState:
        user_id = state.get("user_id", "demo-user")
        state["memory"] = self.memory_store.get_user_memory(user_id)
        return state

    def plan(self, state: DeepAgentState) -> DeepAgentState:
        state["plan"] = decompose_task(state["task"])
        return state

    def select_tools(self, state: DeepAgentState) -> DeepAgentState:
        task = state["task"].lower()
        selected = ["decompose_task"]
        if any(term in task for term in ("mcp", "langgraph", "langchain", "memory", "agent")):
            selected.append("search_knowledge")
        if any(term in task for term in ("risk", "security", "production", "safe", "sql", "pii")):
            selected.append("assess_risks")
        state["selected_tools"] = selected
        return state

    def execute_tools(self, state: DeepAgentState) -> DeepAgentState:
        observations = []
        if "search_knowledge" in state.get("selected_tools", []):
            observations.extend(search_knowledge(state["task"]))
        if "assess_risks" in state.get("selected_tools", []):
            observations.append({"source": "risk_assessment", "findings": assess_risks(state["task"])})
        state["observations"] = observations
        state["citations"] = [
            str(item["source"]) for item in observations if isinstance(item, dict) and "source" in item
        ]
        return state

    def synthesize(self, state: DeepAgentState) -> DeepAgentState:
        is_grounded, fallback = validate_grounding(state["task"], state.get("citations", []))
        if not is_grounded:
            state["answer"] = add_guardrail_note(fallback)
            return state
        plan_lines = "\n".join(f"- {step}" for step in state.get("plan", []))
        observation_lines = []
        for item in state.get("observations", []):
            source = item.get("source", "tool") if isinstance(item, dict) else "tool"
            if "text" in item:
                observation_lines.append(f"- {source}: {item['text'][:350]}")
            elif "findings" in item:
                observation_lines.append(f"- {source}: {item['findings']}")
        observations = "\n".join(observation_lines) or "- No external tool evidence needed."
        state["answer"] = add_guardrail_note(
            "DeepAgent response\n\n"
            "Plan:\n"
            f"{plan_lines}\n\n"
            "Tool observations:\n"
            f"{observations}\n\n"
            "Recommendation:\n"
            "Use a graph-based agent with explicit tool boundaries, MCP-decorated capabilities, "
            "persistent memory, and tests around routing, memory, and tool safety."
        )
        return state

    def save_memory(self, state: DeepAgentState) -> DeepAgentState:
        user_id = state.get("user_id", "demo-user")
        profile = state.get("memory", {})
        profile["last_task_type"] = "deep_agent_analysis"
        self.memory_store.save_user_memory(user_id, profile)
        self.memory_store.save_task_result(user_id, state["task"], state["answer"])
        return state
