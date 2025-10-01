from typing import Annotated

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from app.ai.agents.supervisor.tools.search_internet_tool import search_internet
from app.ai.prompts.supervisor_prompt import SUPERVISOR_PROMPT

load_dotenv()


memory = InMemorySaver()
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
tools = [search_internet]

llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list, add_messages]


async def supervisor(state: State):
    prompt = ChatPromptTemplate.from_template(SUPERVISOR_PROMPT)
    chain = prompt | llm_with_tools

    # Itera sobre os tokens gerados pelo LLM
    async for token in chain.astream({"user_input": state["messages"][-1].content}):
        # Se ainda não existe uma resposta "assistant" no estado, cria

        # Concatena tokens no último content

        state["messages"][-1].content += token.content

        # Yield parcial para o grafo / FastAPI
        yield state


tool_node = ToolNode(tools)
graph_builder = StateGraph(State)

graph_builder.add_node("supervisor", supervisor)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "supervisor")
graph_builder.add_conditional_edges("supervisor", tools_condition)
graph_builder.add_edge("tools", "supervisor")
graph_builder.add_edge("supervisor", END)


supervisor_graph = graph_builder.compile()
