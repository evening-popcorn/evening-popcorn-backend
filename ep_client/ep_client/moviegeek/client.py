import os

import httpx

from ep_client.moviegeek.responses import MovieInfo


class MovieGeekClient:

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=os.environ.get("CLIENT_MOVIEGEEK_URL", "http://moviegeek")
        )

    async def get_movie(self, movie_id: int, locale: str) -> MovieInfo:
        res = await self.client.get(f"/v1/movie/{movie_id}")
        if res.status_code == 200:
            return MovieInfo(**res.json())

    async def close(self):
        await self.client.aclose()
