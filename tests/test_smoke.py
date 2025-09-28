from agents.graphs.main_graph import graph


def test_smoke():
    out = graph.invoke({"goal": "Create a purchase order for 10 steel rods", "approve": True})
    assert "draft" in out