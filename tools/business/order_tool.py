# Example domain tool — replace with your domain logic (ERP/CRM/etc.)


from datetime import datetime


def get_context_for_order(goal: str) -> str:
    # In real builds: query DBs, vector stores (RAG), or external systems here
    return (
        "Company Policy: Standard purchase orders require manager approval over $10k.\n"
        "Inventory: Steel rods in stock: 500 units. Lead time: 3 days.\n"
        f"Timestamp: {datetime.utcnow().isoformat()}Z"
    )




def write_order(order_text: str) -> None:
    # In real builds: persist to DB, emit event, or call ERP API
    print("[write_order]", order_text[:200], "...")