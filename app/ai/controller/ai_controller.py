from typing import Any, Literal, Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import ToolMessage
from langgraph.types import Command, interrupt
from pydantic import BaseModel

from app.ai.agents.comments_agent.comment_agent import comment_agent_graph
from app.ai.agents.general_subject_agent.general_subject_agent import (
    general_subject_agent_compiled,
)
from app.ai.agents.supervisor.supervisor import State, supervisor_graph
from app.ai.utils.token_generator import event_generator

router = APIRouter(prefix="/ai", tags=["AI"])


class supervisorRequest(BaseModel):
    message: str


class resumeRequest(BaseModel):
    action_request: Literal["accept", "reject", "update"]
    data: Optional[Any] = None
    message: Optional[str] = None


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

    return StreamingResponse(
        event_generator(body=body, graph=comment_agent_graph),
        media_type="text/event-stream",
    )

    # response = await comment_agent_graph.ainvoke(
    #     {"messages": [{"role": "user", "content": body.message}]},
    #     {"configurable": {"thread_id": "1"}},
    # )
    # print("===============", response)
    # return {"input": body.message, "response": response["messages"][-1].content}


@router.post("/stream/comment_agent/resume")
async def execute_comment_agent_resume(body: resumeRequest):

    return StreamingResponse(
        event_generator(body=body, graph=comment_agent_graph, resume=True),
        media_type="text/event-stream",
    )

    # response = await comment_agent_graph.ainvoke(
    #     Command(resume=body.model_dump_json()),
    #     {"configurable": {"thread_id": "1"}},
    # )
    # print("===============", response)
    # return {"input": body.message, "response": response["messages"][-1].content}


@router.post("/stream/general_subject_agent")
async def execute_general_subject_agent(body: supervisorRequest):

    return StreamingResponse(
        event_generator(body=body, graph=general_subject_agent_compiled),
        media_type="text/event-stream",
    )


@router.post("/stream/general_subject_agent/resume")
async def execute_general_subject_agent_resume(body: resumeRequest):

    return StreamingResponse(
        event_generator(body=body, graph=general_subject_agent_compiled, resume=True),
        media_type="text/event-stream",
    )
