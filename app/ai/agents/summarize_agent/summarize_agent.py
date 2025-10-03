from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages

from app.ai.prompts.summarize_prompt import SUMMARIZE_PROMPT

load_dotenv()

memory = InMemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


model = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")


async def agent(state: State):

    prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)

    chain = prompt | model

    response = await chain.ainvoke({"msgs": state["messages"][-1].content})

    return {"messages": [response]}


graph_builder = StateGraph(State)


graph_builder.add_node("agent", agent)

graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

summarize_agent_graph = graph_builder.compile()
