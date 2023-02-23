import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.config import POSTGRES_CONFIG
from src.routing import add_routing

app = FastAPI()
add_routing(app)
register_tortoise(
    app,
    db_url=POSTGRES_CONFIG.get_connection_url(),
    modules={"models": ["src.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
