from motor import motor_asyncio as motor

from src.config import MONGO_CONFIG


def mongodb_connection() -> motor.AsyncIOMotorDatabase:
    """
    MongoDB's connection with DB
    """
    client = motor.AsyncIOMotorClient(MONGO_CONFIG.get_connection_url())
    try:
        yield client[MONGO_CONFIG.db_name]
    finally:
        client.close()
