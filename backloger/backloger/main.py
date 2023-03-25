from typing import Dict
from typing import List

import uvicorn
from ep_client.backloger.responses import BacklogCheck
from ep_client.backloger.responses import UserBacklog
from ep_client.responses import SimpleResponse
from fastapi import Body
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query

from uuid import UUID

from backloger.controller import BacklogController

app = FastAPI()


@app.get("/v1/user-backlog")
async def get_movie_info(
    user_id: UUID = Query(),
    page: int = Query(ge=1, default=1),
    controller: BacklogController = Depends()
) -> UserBacklog:
    """
    Get user backlog
    """
    return await controller.get_user_backlog(
        user_id=user_id,
        page=page,
    )


@app.post("/v1/user-backlog")
async def add_to_backlog(
    user_id: UUID = Body(),
    movie_id: int = Body(),
    note: str = Body(max_length=1024),
    controller: BacklogController = Depends()
) -> SimpleResponse:
    """
    Add movie to backlog
    """
    return SimpleResponse(
        success=await controller.add_to_backlog(
            user_id=user_id,
            movie_id=movie_id,
            note=note,
        )
    )


@app.delete("/v1/user-backlog")
async def delete_from_backlog(
    user_id: UUID = Query(),
    movie_id: int = Query(),
    controller: BacklogController = Depends()
) -> SimpleResponse:
    """
    Delete movie from backlog
    """
    return SimpleResponse(
        success=await controller.delete_from_backlog(
            user_id=user_id,
            movie_id=movie_id,
        )
    )


@app.get("/v1/check-is-in-backlog")
async def check_is_in_backlog(
    user_id: UUID = Query(),
    movie_ids: List[int] = Query(),
    controller: BacklogController = Depends()
) -> Dict[str, BacklogCheck]:
    """
    Check is movie in backlog
    """
    return await controller.check_is_movie_in_backlog(
        user_id=user_id,
        movie_ids=movie_ids
    )


if __name__ == "__main__":
    uvicorn.run("backloger.main:app", host="0.0.0.0", port=8082)
