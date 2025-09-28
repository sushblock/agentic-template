from fastapi import FastAPI
from pydantic import BaseModel
from agents.graphs.main_graph import graph


app = FastAPI(title="Agentic Template API")


class RunRequest(BaseModel):
    goal: str
    approve: bool = False


@app.post("/run")
async def run(req: RunRequest):
    state = {"goal": req.goal, "approve": req.approve}
    result = graph.invoke(state)
    return result


@app.get("/health")
async def health():
    return {"status": "ok"}