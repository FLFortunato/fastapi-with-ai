from fastapi import APIRouter
from pydantic import BaseModel

from ..agents.orchestrator import orchestrator_graph

router = APIRouter(prefix="/ai", tags=["AI"])


class OrchestratorRequest(BaseModel):
    message: str


@router.post("/")
async def execute(body: OrchestratorRequest):
    from ..agents.orchestrator import State  # Import State if not already imported

    initial_state = State(
        messages=[{"role": "user", "content": body.message}],
        orchestrator_response=None,
    )

    # Executa o grafo
    final_state = await orchestrator_graph.ainvoke(initial_state)

    return {
        "input": body.message,
        "response": final_state["orchestrator_response"],
    }
