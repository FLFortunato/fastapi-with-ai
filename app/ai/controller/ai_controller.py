from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import ToolMessage
from pydantic import BaseModel

from app.ai.agents.comments_agent.comment_agent import comment_agent_graph
from app.ai.agents.supervisor.supervisor import State, supervisor_graph
from app.ai.utils.token_generator import event_generator

router = APIRouter(prefix="/ai", tags=["AI"])


class supervisorRequest(BaseModel):
    message: str


@router.post("/stream")
async def execute(body: supervisorRequest):

    async def event_generator():

        # Itera sobre o async generator do supervisor
        async for partial_state in supervisor_graph.astream(
            {"messages": [{"role": "user", "content": body.message}]},
            {"configurable": {"thread_id": "1"}},
            stream_mode="messages",
        ):

            state, metadata = (
                partial_state  # 👈 desempacota o retorno (state, metadata)
            )

            # o "state" sim contém as mensagens

            token = getattr(state, "content")  # pega o último chunk gerado

            yield token

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/stream/comment_agent")
async def execute_comment_agent(body: supervisorRequest):
    state = {"messages": [{"role": "user", "content": body.message}]}
    # return StreamingResponse(
    #     event_generator(body=body, graph=comment_agent_graph),
    #     media_type="text/event-stream",
    # )

    response = await comment_agent_graph.ainvoke(
        {"messages": [{"role": "user", "content": body.message}]},
        {"configurable": {"thread_id": "1"}},
    )

    paused = getattr(response, "paused", False)
    current_node = getattr(response, "current_node", None)

    return {
        "paused": paused,
        "next_node": current_node,
        "messages": response.get("messages", []),
    }
