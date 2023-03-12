from pydantic import BaseModel


class UserBacklogDto(BaseModel):
    movie_id: int
    note: str
