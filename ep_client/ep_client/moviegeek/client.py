import os

import httpx

from ep_client.moviegeek.responses import MovieInfo
from ep_client.moviegeek.responses import MovieSearchResult


class MovieGeekClient:

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=os.environ.get("CLIENT_MOVIEGEEK_URL", "http://moviegeek")
        )

    async def get_movie(self, movie_id: int, locale: str) -> MovieInfo:
        res = await self.client.get(f"/v1/movie/{movie_id}", params={
            "locale": locale
        })
        if res.status_code == 200:
            return MovieInfo(**res.json())

    async def search_movie(
        self,
        q: str,
        page: int,
        locale: str,
    ) -> MovieSearchResult:
        res = await self.client.get(f"/v1/movie/search", params={
            "q": q,
            "page": page,
            "locale": locale
        })
        if res.status_code == 200:
            return MovieSearchResult(**res.json())

    async def close(self):
        await self.client.aclose()
