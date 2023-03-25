from typing import Literal

from fastapi import APIRouter, Depends, Body
from fastapi import HTTPException
from pydantic import BaseModel

from api_gateway.controllers.social_auth import EmailNotVerifiedException
from api_gateway.controllers.social_auth import InvalidCodeException
from api_gateway.controllers.social_auth import LoginResponse
from api_gateway.controllers.social_auth import SocialAuthController
from api_gateway.controllers.social_auth import UserNotLinkedOAuthException

router = APIRouter()


class OAuthBody(BaseModel):
    oauth_type: Literal["apple", "google"]
    auth_code: str


@router.post("/login")
async def social_login(
    body: OAuthBody = Body(),
    controller: SocialAuthController = Depends()
) -> LoginResponse:
    try:
        user = await controller.login(
            oauth_type=body.oauth_type,
            auth_code=body.auth_code,
        )
    except InvalidCodeException:
        raise HTTPException(
            status_code=400,
            detail="Invalid code"
        )
    except EmailNotVerifiedException:
        raise HTTPException(
            status_code=400,
            detail="User email not verified"
        )
    except UserNotLinkedOAuthException:
        raise HTTPException(
            status_code=400,
            detail="Account not linked to this OAuth"
        )
    return user


@router.post("service/apple-user-update")
async def apple_user_update():
    # todo treat updates from apple
    pass
