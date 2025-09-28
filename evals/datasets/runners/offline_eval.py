import json
from pathlib import Path
from agents.graphs.main_graph import graph


DATA = Path(__file__).parent.parent / "datasets" / "sample_tasks.jsonl"


if __name__ == "__main__":
    with open(DATA, "r", encoding="utf-8") as f:
        for line in f:
            ex = json.loads(line)
            state = {"goal": ex["goal"], "approve": ex.get("approve", False)}
            out = graph.invoke(state) # type: ignore
            print("=== RESULT ===")
            for k, v in out.items():
                if isinstance(v, str) and len(v) > 300:
                    v = v[:300] + "..."
                print(k, ":", v)