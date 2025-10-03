from typing import List, Union

from langchain.schema import AIMessage, HumanMessage


def format_history_msgs(msgs: List[Union[HumanMessage, AIMessage]]) -> str:
    conversation_text = ""
    for msg in msgs:
        role = "Usuário" if isinstance(msg, HumanMessage) else "Assistente"
        conversation_text += f"{role}: {msg.content}\n"
    return conversation_text
