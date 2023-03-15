from typing import List

import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi.params import Query

from ep_client.moviegeek.responses import MovieInfo
from ep_client.moviegeek.responses import MovieSearchResult
from moviegeek.controllers.movie import MoviesController

app = FastAPI()


@app.get("/v1/movie/search")
async def search_movie(
    q: str = Query(),
    page: int = Query(default=1),
    locale: str = Query(),
    movie_controller: MoviesController = Depends(),
) -> MovieSearchResult:
    return await movie_controller.search_movie(
        query=q,
        page=page,
        locale=locale,
    )


@app.get("/v1/movie/bulk")
async def search_movie(
    movie_ids: List[int] = Query(),
    locale: str = Query(),
    movie_controller: MoviesController = Depends(),
):
    return await movie_controller.get_movies(
        movie_ids=movie_ids,
        locale=locale,
    )


@app.get("/v1/movie/{movie_id}")
async def get_movie_info(
    movie_id: int,
    locale: str = Query(),
    movie_controller: MoviesController = Depends(),
) -> MovieInfo:
    return await movie_controller.get_movie(
        movie_id=movie_id,
        locale=locale,
    )


if __name__ == "__main__":
    uvicorn.run("moviegeek.main:app", host="0.0.0.0", port=8081)
