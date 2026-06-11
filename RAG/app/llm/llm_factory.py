from langchain_openai import ChatOpenAI

from app.config.settings import settings


def get_llm():

    return ChatOpenAI(
        model=settings.llm_model,
        temperature=0,
        api_key=settings.openai_api_key
    )