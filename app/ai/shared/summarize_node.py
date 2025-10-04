import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage


async def summarize_before_model(state, model):
    messages = state["messages"]

    # conversa inteira em texto
    conversation_text = "\n".join(f"{m.type.upper()}: {m.content}" for m in messages)

    # prompt de resumo estruturado
    summary_prompt = f"""
    Resuma a conversa abaixo em até 3 frases curtas,
    e extraia as informações cruciais e importantes.

    CONVERSA:
    {conversation_text}

    """

    result = await model.ainvoke([HumanMessage(content=summary_prompt)])

    # cria mensagem de system com o resumo condensado
    summary_msg = SystemMessage(
        content=result.content,
    )

    return summary_msg
