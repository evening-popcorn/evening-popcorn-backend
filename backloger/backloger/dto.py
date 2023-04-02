from pydantic import BaseModel


class UserBacklogDto(BaseModel):
    """
    User backlog entry dto
    """
    movie_id: int
    note: str
