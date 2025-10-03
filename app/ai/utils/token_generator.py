import json
from typing import Any, AsyncGenerator, Optional

from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, interrupt


async def event_generator(
    graph: CompiledStateGraph,
    body: Any,
    resume: Optional[bool] = False,
    thread_id: int = 1,
) -> AsyncGenerator[str, None]:
    payload = (
        {"messages": [{"role": "user", "content": body.message}]}
        if not resume
        else Command(resume=body.model_dump_json())
    )

    async for kind_or_update in graph.astream(
        payload,
        {"configurable": {"thread_id": str(thread_id)}},
        stream_mode=["messages", "updates"],
    ):

        # Se vier no formato de tupla (messages mode)

        if isinstance(kind_or_update, tuple):

            # Este é (message_chunk, metadata)
            kind, data = kind_or_update
            if (
                kind == "messages"
                and not isinstance(data[0], SystemMessage)
                and not isinstance(data[0], ToolMessage)
            ):

                yield f"{json.dumps({"type": "token", "data": data[0].content})}\n\n"
            elif kind == "updates":
                state = data  # state dict
                # Se houver interrupt, envia para o frontend
                if "__interrupt__" in state:
                    interrupt_tuple = state["__interrupt__"]

                    if isinstance(interrupt_tuple, tuple) and len(interrupt_tuple) > 0:
                        interrupt = interrupt_tuple[0]  # objeto Interrupt
                        yield f"{json.dumps(
                            {
                                "type": "interrupt",
                                "question": interrupt.value.get("question"),
                                "tool_call": interrupt.value.get("tool_call"),
                            }
                        )}\n\n"
