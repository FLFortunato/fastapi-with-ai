SUMMARIZE_PROMPT = """
    Resuma a conversa abaixo em até 3 frases curtas,
    e extraia uma lista de fatos importantes (empresas, cotações, intenções do usuário).

    CONVERSA:
    {msgs}

    Responda em JSON:
    {{
      "summary": "...",
      "facts": ["...", "..."]
    }}
    """
