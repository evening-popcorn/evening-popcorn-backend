import os
from typing import Dict
from typing import List
from uuid import UUID

import httpx

from ep_client.backloger.responses import BacklogCheck
from ep_client.backloger.responses import UserBacklog


class BacklogerClient:
    """
    Client for Backloger microservice
    """

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=os.environ.get("CLIENT_BACKLOGER_URL", "http://moviegeek")
        )

    async def get_user_backlog(
        self, user_id: UUID, page: int = 1
    ) -> UserBacklog:
        """
        Get user backlog
        """
        res = await self.client.get("/v1/user-backlog", params={
            "user_id": user_id,
            "page": page,
        })
        if res.status_code == 200:
            return UserBacklog(**res.json())

    async def add_to_backlog(
        self,
        user_id: UUID,
        movie_id: int,
        note: str,
    ) -> bool:
        """
        Add movie to backlog
        """
        res = await self.client.post(
            "/v1/user-backlog",
            json={
                "user_id": str(user_id),
                "movie_id": movie_id,
                "note": note
            }
        )
        if res.status_code == 200:
            return res.json()["success"]

    async def delete_from_backlog(
        self,
        user_id: UUID,
        movie_id: int,
    ) -> bool:
        """
        Delete movie from backlog
        """
        res = await self.client.delete(
            "/v1/user-backlog",
            params={
                "user_id": user_id,
                "movie_id": movie_id,
            }
        )
        if res.status_code == 200:
            return res.json()["success"]

    async def check_is_in_backlog(
        self,
        user_id: UUID,
        movie_ids: List[int],
    ) -> Dict[int, BacklogCheck]:
        """
        Check if movie is in backlog
        """
        res = await self.client.get(
            "/v1/check-is-in-backlog",
            params={
                "user_id": user_id,
                "movie_ids": movie_ids,
            }
        )
        if res.status_code == 200:
            return {
                int(movie_id): BacklogCheck(**status)
                for movie_id, status in res.json().items()
            }
