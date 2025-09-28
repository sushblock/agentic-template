import argparse
from agents.graphs.main_graph import graph


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--goal", required=True)
    p.add_argument("--approve", action="store_true")
    args = p.parse_args()


    state = {"goal": args.goal, "approve": args.approve}
    out = graph.invoke(state) # type: ignore
    print(out)