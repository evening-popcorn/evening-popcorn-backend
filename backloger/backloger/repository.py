from datetime import datetime
from typing import Tuple
from uuid import UUID
from enum import StrEnum
from typing import Dict
from typing import List

from asyncpg import Connection
from asyncpg import UniqueViolationError
from fastapi import Depends

from backloger.config import pg_connection
from backloger.dto import UserBacklogDto


class BacklogOrder(StrEnum):
    added_at_desc = "added_at DESC"
    added_at_asc = "added_at ASC"


class BacklogRepository:

    def __init__(self, pg_conn: Connection = Depends(pg_connection)) -> None:
        self.pg_conn = pg_conn

    async def get_user_backlog_size(self, user_id: UUID) -> int:
        sql = """
            SELECT count(*) as size
            FROM users_backlog
            WHERE user_id = $1
        """
        res = await self.pg_conn.fetch(sql, user_id)
        return res[0]["size"]

    async def get_users_backlog(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        order_by: BacklogOrder = BacklogOrder.added_at_asc
    ) -> List[UserBacklogDto]:
        sql = """
            SELECT movie_id, note
            FROM users_backlog
            WHERE user_id = $1
            ORDER BY $2
            LIMIT $3
            OFFSET $4
        """
        res = await self.pg_conn.fetch(sql, user_id, order_by, limit, offset)
        return [
            UserBacklogDto(
                movie_id=info["movie_id"],
                note=info["note"],
            )
            for info in res
        ]

    async def check_is_in_backlog(
        self,
        user_id: UUID,
        movie_ids: List[int]
    ) -> Dict[int, Tuple[bool, str]]:
        sql = """
            SELECT movie_id, note
            FROM users_backlog
            WHERE user_id = $1 
                and movie_id = any($2::int[])
        """
        res = await self.pg_conn.fetch(sql, user_id, movie_ids)
        backlog = {movie["movie_id"]: movie["note"] for movie in res}
        return {
            movie_id: ((movie_id in backlog), backlog.get(movie_id))
            for movie_id in movie_ids
        }

    async def add_to_backlog(
        self,
        user_id: UUID,
        movie_id: int,
        note: str
    ) -> bool:
        sql = """
            INSERT INTO users_backlog (user_id, movie_id, note, added_at) 
            VALUES ($1, $2, $3, $4) 
        """
        try:
            await self.pg_conn.execute(
                sql, user_id, movie_id, note, datetime.now()
            )
        except UniqueViolationError:
            return False
        return True

    async def update_note_in_backlog(
        self,
        user_id: UUID,
        movie_id: int,
        note: str
    ) -> bool:
        sql = """
            UPDATE public.users_backlog
            SET note = $1
            WHERE user_id = $2
              AND movie_id = $3;
        """
        res = await self.pg_conn.execute(
            sql, note, user_id, movie_id,
        )
        return res.split()[-1] == "1"

    async def remove_from_backlog(
        self,
        user_id: UUID,
        movie_id: int
    ) -> bool:
        sql = """
            DELETE FROM users_backlog
            WHERE user_id = $1
              AND movie_id = $2
        """
        res = await self.pg_conn.execute(
            sql, user_id, movie_id
        )
        return res.split()[-1] == "1"
