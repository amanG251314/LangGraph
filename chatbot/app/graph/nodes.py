from langchain_core.messages import (
    SystemMessage
)

from langchain_openai import ChatOpenAI

from app.config.settings import settings


SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer clearly and concisely.
"""


llm = ChatOpenAI(
    model=settings.MODEL_NAME,
    api_key=settings.OPENAI_API_KEY,
    temperature=0
)


def chatbot_node(state):

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        )
    ] + state["messages"]

    response = llm.invoke(
        messages
    )

    return {
        "messages": [response]
    }