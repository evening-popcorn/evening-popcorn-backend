import uvicorn
from fastapi import Depends
from fastapi import FastAPI

from src.controllers.movie import MoviesController

app = FastAPI()


@app.get("/v1/movie/{movie_id}")
async def get_movie_info(
    movie_id: int,
    movie_controller: MoviesController = Depends(),
):
    return await movie_controller.get_movie(
        movie_id=movie_id,
        locale="RU",
    )


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080)
