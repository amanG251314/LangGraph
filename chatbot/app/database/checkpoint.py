import psycopg

from langgraph.checkpoint.postgres import (
    PostgresSaver
)

from app.config.settings import settings

# utility class with static factory methods to manage checkpointer creation and initialization
class CheckpointManager:

    @staticmethod
    def create():

        conn = psycopg.connect(
            settings.postgres_uri,
            autocommit=True
        )

        return PostgresSaver(conn)

    @staticmethod
    def initialize():

        checkpointer = (
            CheckpointManager.create()
        )

        checkpointer.setup()

        return checkpointer