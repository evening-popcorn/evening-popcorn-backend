from datetime import datetime
from datetime import timedelta
from enum import StrEnum
from typing import List

import httpx
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from moviegeek.config import TMDB_CONFIG
from moviegeek.depends.mongodb_connection import mongodb_connection
from moviegeek.repositories.dto.tmdb import Movie
from moviegeek.repositories.dto.tmdb import MovieSearchResult


class TMDBRepository:
    """
    Repository for The Movie DB
    """
    def __init__(
        self,
        mongo_connection: AsyncIOMotorDatabase = Depends(mongodb_connection),
    ) -> None:
        self.mongo_connection = mongo_connection
        self.client = httpx.AsyncClient(
            base_url="https://api.themoviedb.org/3/",
            params={
                "api_key": TMDB_CONFIG.api_key
            }
        )

    async def get_movie(
        self,
        movie_id: int,
        locale: str,
    ) -> Movie:
        """
        Get movie info
        """
        obj = await self.mongo_connection["movies_cache"].find_one({
            "_id": f"{movie_id}/{locale}",
        })
        if (create := not obj) or obj["store_until"] < datetime.now():
            res = (await self.client.get(
                f"movie/{movie_id}",
                params={
                    "language": locale,
                    "append_to_response": "watch/providers,credits"
                }
            ))
            if res.status_code != 200:
                raise RuntimeError
            obj = res.json()
            providers = obj["watch/providers"]["results"].get(locale.upper(), dict())
            watch_providers = (
                    providers.get("flatrate", [])
                    + providers.get("rent", [])
                    + providers.get("buy", [])
            )
            providers_map = dict()
            for wp in watch_providers:
                if wp["provider_id"] not in providers_map:
                    providers_map[wp["provider_id"]] = wp
            obj["watch_providers"] = sorted(
                providers_map.values(),
                key=lambda el: el["display_priority"]
            )
            parsed_obj = Movie(**obj)
            if create:
                await self.mongo_connection["movies_cache"].insert_one(
                    {
                        "_id": f"{movie_id}/{locale}",
                        "store_until": datetime.now() + timedelta(days=7),
                        **parsed_obj.dict()
                    }
                )
            else:
                await self.mongo_connection["movies_cache"].replace_one(
                    {"_id": f"{movie_id}/{locale}"},
                    {
                        "store_until": datetime.now() + timedelta(days=7),
                        **parsed_obj.dict()
                    }
                )
            return parsed_obj

        obj["id"] = int(obj["_id"].split("/")[0])
        return Movie(**obj)

    async def search_movie(
        self, query: str, locale: str, page: int
    ) -> MovieSearchResult:
        """
        Search movie
        """
        params = {
                "query": query,
                "language": locale,
            }
        if page > 1:
            params["page"] = page
        res = await self.client.get(
            "search/movie",
            params=params
        )
        if res.status_code != 200:
            raise RuntimeError
        return MovieSearchResult(**res.json())
