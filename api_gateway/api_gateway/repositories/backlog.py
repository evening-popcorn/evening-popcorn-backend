import uuid
from typing import Dict
from typing import List

from ep_client.backloger.client import BacklogerClient
from fastapi import Depends
from api_gateway.repositories.dto.backlog import Backlog
from api_gateway.repositories.dto.backlog import BacklogStatus


class BacklogRepository:
    def __init__(self, backloger_client: BacklogerClient = Depends()) -> None:
        self.backloger_client = backloger_client

    async def get_user_backlog(
        self,
        user_id: uuid.UUID,
        page: int = 1
    ) -> Backlog:
        """
        Get user backlog
        """
        res = await self.backloger_client.get_user_backlog(
            user_id=user_id,
            page=page
        )
        return Backlog(
            page=res.page,
            total_pages=res.total_pages,
            backlog=[
                BacklogStatus(
                    movie_id=entry.movie_id,
                    in_backlog=True,
                    note=entry.note
                )
                for entry in res.result
            ]
        )

    async def get_movie_status(
        self,
        movie_id: int,
        user_id: uuid.UUID
    ) -> BacklogStatus:
        """
        Get movie status
        """
        res = (await self.backloger_client.check_is_in_backlog(
            movie_ids=[movie_id],
            user_id=user_id,
        ))[movie_id]
        return BacklogStatus(
            movie_id=movie_id,
            in_backlog=res.in_backlog,
            note=res.note
        )

    async def bulk_get_movie_status(
        self,
        movie_ids: List[int],
        user_id: uuid.UUID,
    ) -> Dict[int, BacklogStatus]:
        """
        Bulk get movie status
        """
        res = await self.backloger_client.check_is_in_backlog(
            user_id=user_id,
            movie_ids=movie_ids
        )
        return {
            movie_id: BacklogStatus(
                movie_id=movie_id,
                in_backlog=status.in_backlog,
                note=status.note
            )
            for movie_id, status in res.items()
        }

    async def add_to_backlog(
        self,
        user_id: uuid.UUID,
        movie_id: int,
        note: str
    ) -> bool:
        """
        Add movie to backlog
        """
        return await self.backloger_client.add_to_backlog(
            user_id=user_id,
            movie_id=movie_id,
            note=note
        )

    async def remove_from_backlog(
        self,
        user_id: uuid.UUID,
        movie_id: int,
    ) -> bool:
        return await self.backloger_client.delete_from_backlog(
            user_id=user_id,
            movie_id=movie_id
        )
