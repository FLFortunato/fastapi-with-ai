from typing import Annotated, Optional

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from app.ai.prompts.orchestrator_prompt import ORCHESTRATOR_PROMPT

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


class OrchestratorResponse(BaseModel):
    sub_agents: list[str] = Field(
        description="""
 Lista que contém os nomes dos subagentes que serão necessários para atender às necessidades do usuário.
 post_agent: Subagente responsável por tudo que tem a ver com posts;
 comment_agent: Subagente responsável por tudo que tenha relação com comentários."""
    )
    response: Optional[str] = Field(
        description="Se nenhum agente precisar ser chamado, retornar uma resposta amigável ao usuário com base na solicitação."
    )


class State(TypedDict):
    messages: Annotated[list, add_messages]
    orchestrator_response: Optional[OrchestratorResponse]


async def orchestrator(state: State):

    parser = PydanticOutputParser(pydantic_object=OrchestratorResponse)

    prompt = ChatPromptTemplate.from_template(ORCHESTRATOR_PROMPT)

    chain = prompt | llm | parser

    response = await chain.ainvoke(
        {
            "user_input": state["messages"][-1].content or "",
            "format_instructions": parser.get_format_instructions(),
        }
    )

    return {"orchestrator_response": response}


graph_builder = StateGraph(State)

graph_builder.add_node("orchestrator", orchestrator)

graph_builder.add_edge(START, "orchestrator")
graph_builder.add_edge("orchestrator", END)


orchestrator_graph = graph_builder.compile()
