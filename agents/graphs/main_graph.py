from langgraph.graph import StateGraph, END
from agents.state import AppState
from models.llm_adapter import LLM
from tools.business.order_tool import get_context_for_order, write_order
from agents.policies import guard
from rag.retriever import retrieve


llm = LLM.from_env()


def plan(state: AppState):
    steps = llm.plan(state["goal"], tools=["get_context_for_order", "write_order"])
    return {**state, "plan": steps}


def act(state: AppState):
    # Get domain-specific context
    domain_ctx = get_context_for_order(state["goal"])
    
    # Get RAG context from vector store
    rag_ctx = retrieve(state["goal"])
    
    # Combine contexts
    combined_ctx = f"Domain Context:\n{domain_ctx}\n\nRAG Context:\n{rag_ctx}"
    
    draft = llm.solve(goal=state["goal"], context=combined_ctx)
    return {**state, "ctx": combined_ctx, "draft": draft}


def validate(state: AppState):
    return guard(state)


def commit(state: AppState):
    if state.get("approve") and state.get("ok"):
        write_order(state["draft"]) # side effect
    return state


# Build graph
_g = StateGraph(AppState)
_g.add_node("plan", plan)
_g.add_node("act", act)
_g.add_node("validate", validate)
_g.add_node("commit", commit)
_g.set_entry_point("plan")
_g.add_edge("plan", "act")
_g.add_edge("act", "validate")
_g.add_conditional_edges("validate", lambda s: "commit" if s.get("ok") else END, {"commit": "commit"})


graph = _g.compile() # add checkpointer for durability if needed