from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    MODEL_NAME: str = os.getenv(
        "MODEL_NAME",
        "gpt-4o"
    )

    POSTGRES_HOST: str = os.getenv(
        "POSTGRES_HOST"
    )

    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT"
    )

    POSTGRES_DB: str = os.getenv(
        "POSTGRES_DB"
    )

    POSTGRES_USER: str = os.getenv(
        "POSTGRES_USER"
    )

    POSTGRES_PASSWORD: str = os.getenv(
        "POSTGRES_PASSWORD"
    )

    @property
    def postgres_uri(self):

        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()