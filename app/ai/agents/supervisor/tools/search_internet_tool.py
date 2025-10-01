from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langgraph.types import interrupt

load_dotenv()


@tool
async def search_internet(input: str):
    """
    Performs an internet search to retrieve up-to-date information.

    Guidelines:
    - Use this tool only for questions that require recent data.
    - Do not use this tool for general definitions or historical concepts, since the LLM already knows them.
    - Always return the most relevant and concise information found online.
    - Avoid speculation; if information is not found, indicate that clearly.

    Example queries:
    - "Qual a inflação acumulada no Brasil em 2025?"
    - "Quais ações tiveram maior valorização esta semana?"
    - "Quais são as notícias mais recentes sobre o mercado financeiro?"
    - "Qual a cotação do dólar hoje?"

    Parameters:
    ----------
    input : str
        The user query that requires updated information from the internet.

    Returns:
    -------
    str
        A concise, accurate summary of the information retrieved from the internet.
    """

    print("[search_internet]: Executing tool...")
    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general", 
        include_answer=True,
        include_raw_content="markdown",
        include_images=False,
    )

    # Executa a busca e retorna o resultado
    results = await tavily_search_tool.arun(input)
    print("[search_internet]: Finished executing tool...")
    return results
