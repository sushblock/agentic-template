from guardrails.pii import redact_pii
from guardrails.safety import is_safe


POLICY_REFUSAL = "Cannot proceed due to policy/safety violations."


def guard(state: dict) -> dict:
    # Redact sensitive input before model + ensure output safety
    goal = state.get("goal", "")
    red_goal, _ = redact_pii(goal)


    draft = state.get("draft", "")
    red_draft, _ = redact_pii(draft)


    if not is_safe(red_goal) or not is_safe(red_draft):
        state.update({"ok": False, "refusal_reason": POLICY_REFUSAL})
    else:
        state.update({"ok": True, "goal": red_goal, "draft": red_draft})
    return state