import psycopg

from langgraph.checkpoint.postgres import PostgresSaver

from app.config.settings import settings


def get_checkpointer():

    conn = psycopg.connect(
        settings.postgres_uri,
        autocommit=True
    )

    cp = PostgresSaver(conn)
    cp.setup()

    return cp
