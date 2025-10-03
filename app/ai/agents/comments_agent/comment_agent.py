import json
from typing import Annotated, Literal, TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

from app.ai.agents.comments_agent.tools.create_comment import handle_create_comment
from app.ai.agents.supervisor.tools.search_internet_tool import search_internet
from app.ai.prompts.comment_aget_prompt import COMMENT_AGENT_PROMPT
from app.ai.utils.format_history import format_history_msgs

llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")

memory = InMemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    print("==================Human=============CALLED =")
    human_response = interrupt({"query": query})
    return human_response["data"]


tools = [handle_create_comment, search_internet, human_assistance]

llm_with_tools = llm.bind_tools(tools=tools)


async def comment_agent(state: State):

    prompt = ChatPromptTemplate.from_template(COMMENT_AGENT_PROMPT)
    chain = prompt | llm_with_tools

    conversation_history = format_history_msgs([*state["messages"]])

    response = await chain.ainvoke(
        {
            "user_input": state["messages"][-1].content,
            "conversation_history": conversation_history,
        }
    )

    return {"messages": [response]}


def tool_router(state: State):
    """Route to human review if there are tool calls, otherwise end the conversation."""


def route_after_llm(state) -> Literal[END, "human_review_node"]:
    """Route to human review if there are tool calls, otherwise end the conversation."""
    if len(state["messages"][-1].tool_calls) == 0:
        return END
    else:
        return "human_review_node"


async def run_tool(state):
    """Execute the tool call using the appropriate tool."""
    new_messages = []
    tools = {"search_internet": search_internet}
    tool_calls = state["messages"][-1].tool_calls
    for tool_call in tool_calls:
        tool = tools[tool_call["name"]]
        result = await tool.ainvoke(tool_call["args"])
        new_messages.append(
            {
                "role": "tool",
                "name": tool_call["name"],
                "content": result,
                "tool_call_id": tool_call["id"],
            }
        )
    return {"messages": new_messages}


def human_review_node(state) -> Command[Literal["comment_agent", "run_tool"]]:
    """Allow human review of tool calls before execution."""
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[-1]
    # this is the value we'll be providing via Command(resume=<human_review>)

    human_review = interrupt(
        {
            "question": "Is this correct?",
            # Surface tool calls for review
            "tool_call": tool_call,
        }
    )
    print("===========CHECKING==========", human_review)
    valid_dict = json.loads(human_review)

    review_action = valid_dict.get("action")
    review_data = valid_dict.get("data")
    # if approved, call the tool
    if review_action == "continue":
        return Command(goto="run_tool")
    # update the AI message AND call tools
    elif review_action == "update":
        updated_message = {
            "role": "ai",
            "content": last_message.content,
            "tool_calls": [
                {
                    "id": tool_call["id"],
                    "name": tool_call["name"],
                    # This the update provided by the human
                    "args": review_data,
                }
            ],
            # This is important - this needs to be the same as the message you replacing!
            # Otherwise, it will show up as a separate message
            "id": last_message.id,
        }
        return Command(goto="run_tool", update={"messages": [updated_message]})
    # provide feedback to LLM
    elif review_action == "feedback":
        # NOTE: we're adding feedback message as a ToolMessage
        # to preserve the correct order in the message history
        # (AI messages with tool calls need to be followed by tool call messages)
        tool_message = {
            "role": "tool",
            # This is our natural language feedback
            "content": review_data,
            "name": tool_call["name"],
            "tool_call_id": tool_call["id"],
        }
        return Command(goto="comment_agent", update={"messages": [tool_message]})
    # Default fallback to avoid returning None
    return Command(goto="comment_agent")


tool_node = ToolNode(tools=tools)
graph_builder = StateGraph(State)

graph_builder.add_node("comment_agent", comment_agent)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("human_review_node", human_review_node)
graph_builder.add_node("run_tool", run_tool)


graph_builder.add_edge(START, "comment_agent")
graph_builder.add_conditional_edges("comment_agent", route_after_llm)
graph_builder.add_edge("run_tool", "comment_agent")
graph_builder.add_edge("comment_agent", END)

comment_agent_graph = graph_builder.compile(checkpointer=memory)
