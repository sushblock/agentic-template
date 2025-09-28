from typing import Optional, TypedDict


class AppState(TypedDict, total=False):
    goal: str
    plan: str
    ctx: str
    draft: str
    ok: bool
    approve: bool
    refusal_reason: Optional[str]