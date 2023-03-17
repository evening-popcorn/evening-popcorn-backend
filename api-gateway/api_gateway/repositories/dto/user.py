from uuid import UUID

from pydantic import BaseModel

from api_gateway.models.user import Users


class UserDto(BaseModel):
    id: str
    email: str
    name: str

    def __init__(self, model: Users) -> None:
        super().__init__(
            id=str(model.id),
            email=model.email,
            name=model.name,
        )
