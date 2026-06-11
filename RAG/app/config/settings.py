from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    postgres_uri: str

    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o"

    pdf_dir: str = "data/pdfs"
    cache_dir: str = "cache"

    class Config:
        env_file = ".env"


settings = Settings()