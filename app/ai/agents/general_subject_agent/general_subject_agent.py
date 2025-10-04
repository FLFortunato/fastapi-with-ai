from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from app.ai.agents.general_subject_agent.tools.sum_tool import sum_tool
from app.ai.agents.summarize_agent.summarize_agent import summarize_agent_graph
from app.ai.agents.supervisor.tools.search_internet_tool import search_internet
from app.ai.prompts.general_subject_agent_prompt import GENERAL_SUBJECT_AGENT_PROMPT
from app.ai.shared.summarize_node import summarize_before_model
from app.ai.utils.format_history import format_history_msgs
from app.ai.utils.hitl_wrapper import add_human_in_the_loop

load_dotenv()

memory = InMemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


tools = [add_human_in_the_loop(search_internet), add_human_in_the_loop(sum_tool)]

model = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")


def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:

    prompt = ChatPromptTemplate.from_template(GENERAL_SUBJECT_AGENT_PROMPT)

    chat_history = format_history_msgs([*state["messages"]])

    formatted_propmpt = prompt.invoke(
        {"user_msg": state["messages"][-1].content, "chat_history": chat_history}
    ).to_string()

    return [{"role": "system", "content": formatted_propmpt}] + list(
        state["messages"]
    )  # pyright: ignore[reportReturnType]


async def summarize_node(state: State):
    messages = state["messages"]

    if len(messages) <= 5:
        return {"messages": messages}

    # últimas 3 mensagens brutas
    last_messages = messages[-3:]

    # conversa inteira em texto
    conversation_text = "\n".join(f"{m.type.upper()}: {m.content}" for m in messages)
    summary = await summarize_agent_graph.ainvoke(
        {"messages": [{"role": "user", "content": conversation_text}]}
    )

    new_messages = [
        SystemMessage(content=summary["messages"][-1].content)
    ] + last_messages

    return {"messages": new_messages}


general_subject_agent_compiled = create_react_agent(
    model=model,
    tools=tools,
    prompt=prompt,  # pyright: ignore[reportArgumentType]
    checkpointer=memory,
    pre_model_hook=summarize_node,
)
