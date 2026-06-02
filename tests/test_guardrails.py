from app.services.guardrails import GUARDRAIL_NOTE, add_guardrail_note, validate_grounding


def test_guardrail_note_is_added_once():
    answer = add_guardrail_note("Answer")
    assert GUARDRAIL_NOTE in answer
    assert add_guardrail_note(answer).count(GUARDRAIL_NOTE) == 1


def test_grounding_required_for_agent_tasks():
    is_grounded, message = validate_grounding("Design MCP agent memory", [])
    assert not is_grounded
    assert "grounded tool/resource evidence" in message


def test_grounding_passes_with_citations():
    is_grounded, message = validate_grounding("Design MCP agent memory", ["mcp_design.md"])
    assert is_grounded
    assert message == ""
