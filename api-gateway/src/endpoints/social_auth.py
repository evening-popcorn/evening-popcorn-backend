from typing import Literal

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel


from src.controllers.social_auth import SocialAuthController

router = APIRouter()


class OAuthBody(BaseModel):
    socialNetwork: Literal["apple", "google"]
    authCode: str


@router.post("/login")
async def social (
    body: OAuthBody = Body(),
    controller: SocialAuthController = Depends()
):
    return controller.login(
        socialNetwork=body.socialNetwork,
        authCode=body.authCode
    )


@router.post("service/apple-user-update")
async def google_auth():
    pass
