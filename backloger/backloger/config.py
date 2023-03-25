import asyncpg
from asyncpg import Connection
from ep_utils.configs import PostgresConfig
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONFIG = PostgresConfig()


async def pg_connection() -> Connection:
    """
    Postgres connection dependency
    """
    conn = await asyncpg.connect(POSTGRES_CONFIG.get_connection_url())
    return conn
