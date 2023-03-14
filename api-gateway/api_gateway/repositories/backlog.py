import uuid
from typing import List

from api_gateway.repositories.dto.backlog import BacklogStatus


class BacklogRepository:
    def __init__(self) -> None:
        pass

    async def get_movie_status(
        self,
        movie_id: int,
        user_id: uuid.uuid4
    ) -> BacklogStatus:
        return BacklogStatus(
            movie_id=movie_id,
            in_backlog=False,
        )

    async def bulk_get_movie_status(
        self, movie_ids: List[int], user_id: uuid.uuid4
    ) -> List[BacklogStatus]:
        return [
            BacklogStatus(
                movie_id=movie_id,
                in_backlog=False,
            )
            for movie_id in movie_ids
        ]
