import uuid

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi.params import Param

from ep_client.moviegeek.responses import MovieInfo
from uuid import UUID

from backloger.controller import BacklogController
from backloger.repository import BacklogRepository

app = FastAPI()


@app.get("/v1/user-backlog")
async def get_movie_info(
    user_id: UUID = Param(),
    controller: BacklogController = Depends()
):
    return await repository.remove_from_backlog(user_id=user_id, movie_id=161)


if __name__ == "__main__":
    uvicorn.run("backloger.main:app", host="0.0.0.0", port=8082)
