from typing import Any, AsyncGenerator

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph.state import CompiledStateGraph


async def event_generator(
    graph: CompiledStateGraph,
    body: Any,
    thread_id: int = 1,
) -> AsyncGenerator[str, None]:
    async for partial_state in graph.astream(
        {"messages": [{"role": "user", "content": body.message}]},
        {"configurable": {"thread_id": f"{thread_id}"}},
        stream_mode="messages",
    ):
        state, metadata = partial_state

        token = getattr(state, "content")
        # Verify if it is a tool message, if so, do not show the token
        if not isinstance(state, ToolMessage):
            yield token
