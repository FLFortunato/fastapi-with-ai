import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage


async def summarize_before_model(messages: list[Any], model):

    # regra: só resumir se já passou de 5 mensagens
    if len(messages) <= 1:
        return {"messages": messages}

    # últimas 3 mensagens brutas
    last_messages = messages[-3:]

    # conversa inteira em texto
    conversation_text = "\n".join(f"{m.type.upper()}: {m.content}" for m in messages)

    # prompt de resumo estruturado
    summary_prompt = f"""
    Resuma a conversa abaixo em até 3 frases curtas,
    e extraia uma lista de fatos importantes (empresas, cotações, intenções do usuário).

    CONVERSA:
    {conversation_text}

    Responda em JSON:
    {{
      "summary": "...",
      "facts": ["...", "..."]
    }}
    """

    result = await model.ainvoke([HumanMessage(content=summary_prompt)])

    try:
        data = json.loads(result.content)
    except Exception:
        # fallback se o modelo não responder JSON válido
        data = {"summary": result.content, "facts": []}

    # cria mensagem de system com o resumo condensado
    summary_msg = SystemMessage(
        content=f"Resumo até agora: {data['summary']}\nFatos: {data['facts']}",
    )

    # novo histórico: resumo + últimas mensagens
    print("RESUMO==================", summary_msg)
    new_messages = [summary_msg] + last_messages
    return {"messages": new_messages}
