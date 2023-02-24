from datetime import datetime
from datetime import timedelta
from enum import StrEnum
from typing import List

import httpx
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.config import TMDB_CONFIG
from src.depends.mongodb_connection import mongodb_connection
from src.repositories.dto.tmdb import Movie


class MovieAdditionalInfo(StrEnum):
    watch_providers = "watch/providers"
    credits = ""


class TMDBRepository:
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
        obj = await self.mongo_connection["movies_cache"].find_one({
            "_id": f"{movie_id}/{locale}",
        })
        if (create := not obj) or obj["store_until"] < datetime.now():
            obj = (await self.client.get(
                f"movie/{movie_id}",
                params={
                    "language": locale,
                    "append_to_response": "watch/providers,credits"
                }
            )).json()
            obj["_id"] = f"{movie_id}/{locale}"
            obj["store_until"] = datetime.now() + timedelta(days=7)
            if create:
                res = await self.mongo_connection["movies_cache"].insert_one(obj)
                print(res)
            else:
                await self.mongo_connection["movies_cache"].replace_one(
                    {"_id": f"{movie_id}/{locale}"},
                    obj
                )
        else:
            obj["id"] = int(obj["_id"].split("/")[0])
        return Movie(**obj)
