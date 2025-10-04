import json
from typing import Callable

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_core.tools import tool as create_tool
from langgraph.prebuilt.interrupt import HumanInterrupt, HumanInterruptConfig
from langgraph.types import interrupt


def add_human_in_the_loop(
    tool: Callable | BaseTool,
    *,
    interrupt_config: HumanInterruptConfig = None,
) -> BaseTool:
    """Wrap a tool to support human-in-the-loop review."""

    if not isinstance(tool, BaseTool):
        tool = create_tool(tool)

    if interrupt_config is None:
        interrupt_config = {
            "allow_accept": True,
            "allow_edit": True,
            "allow_respond": True,
        }

    @create_tool(tool.name, description=tool.description, args_schema=tool.args_schema)
    async def call_tool_with_interrupt(config: RunnableConfig, **tool_input):
        request: HumanInterrupt = {
            "action_request": {"action": tool.name, "args": tool_input},
            "config": interrupt_config,
            "description": "Please review the tool call",
        }
        response = interrupt(request)

        formatted_response = (
            json.loads(response) if isinstance(response, str) else response
        )
        # approve the tool call
        print(formatted_response["action_request"] == "accept")
        if formatted_response["action_request"] == "accept":
            tool_response = await tool.ainvoke(tool_input, config)
        # update tool call args
        elif formatted_response["action_request"] == "edit":
            tool_input = formatted_response["args"]["args"]
            tool_response = await tool.ainvoke(tool_input, config)
        # respond to the LLM with user feedback
        elif formatted_response["action_request"] == "response":
            user_feedback = formatted_response["args"]
            tool_response = user_feedback
        else:
            raise ValueError(
                f"Unsupported interrupt response action_request: {formatted_response['action_request']}"
            )

        return tool_response

    return call_tool_with_interrupt
