from math import ceil
from typing import Dict
from typing import List
from uuid import UUID

from ep_client.backloger.responses import BacklogCheck
from ep_client.backloger.responses import BacklogEntry
from fastapi import Depends

from backloger.repository import BacklogOrder
from backloger.repository import BacklogRepository
from ep_client.backloger.responses import UserBacklog

PAGE_SIZE = 20


class BacklogController:
    def __init__(
        self, backlog_repository: BacklogRepository = Depends()
    ) -> None:
        self.backlog_repository = backlog_repository

    async def get_user_backlog(
        self, user_id: UUID, page: int = 1
    ) -> UserBacklog:
        total_size = await self.backlog_repository \
            .get_user_backlog_size(user_id)
        backlog = await self.backlog_repository.get_users_backlog(
            user_id=user_id,
            offset=(page - 1) * PAGE_SIZE,
            limit=PAGE_SIZE,
            order_by=BacklogOrder.added_at_desc
        )
        return UserBacklog(
            page=page,
            total_pages=ceil(total_size / PAGE_SIZE),
            result=[
                BacklogEntry(
                    movie_id=entry.movie_id,
                    note=entry.note,
                )
                for entry in backlog
            ]
        )

    async def add_to_backlog(
        self, user_id: UUID, movie_id: int, note: str
    ) -> bool:
        in_backlog, _ = (await self.backlog_repository.check_is_in_backlog(
            user_id=user_id,
            movie_ids=[movie_id]
        ))[movie_id]
        if not in_backlog:
            res = await self.backlog_repository.add_to_backlog(
                user_id=user_id,
                movie_id=movie_id,
                note=note,
            )
        else:
            res = await self.backlog_repository.update_note_in_backlog(
                user_id=user_id,
                movie_id=movie_id,
                note=note,
            )
        return res

    async def check_is_movie_in_backlog(
        self, user_id: UUID, movie_ids: List[int]
    ) -> Dict[str, BacklogCheck]:
        res = await self.backlog_repository.check_is_in_backlog(
            user_id=user_id,
            movie_ids=movie_ids
        )
        return {
            id: BacklogCheck(
                in_backlog=in_backlog,
                note=note
            )
            for id, (in_backlog, note) in res.items()
        }
