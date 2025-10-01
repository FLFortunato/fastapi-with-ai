from typing import Annotated, TypedDict

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
from app.ai.utils.hitl_wrapper import add_human_in_the_loop

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


tools = [
    handle_create_comment,
    add_human_in_the_loop(search_internet),
    human_assistance,
]

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


tool_node = ToolNode(tools=tools)
graph_builder = StateGraph(State)

graph_builder.add_node("comment_agent", comment_agent)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "comment_agent")
graph_builder.add_conditional_edges("comment_agent", tools_condition)
graph_builder.add_edge("tools", "comment_agent")
graph_builder.add_edge("comment_agent", END)

comment_agent_graph = graph_builder.compile(checkpointer=memory)
