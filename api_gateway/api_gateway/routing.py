from fastapi import APIRouter
from fastapi import FastAPI

from api_gateway.endpoints import movie
from api_gateway.endpoints import social_auth
from api_gateway.endpoints import backlog
from api_gateway.endpoints import auth


def add_routing(app: FastAPI):
    """
    Init app routing
    """
    router = APIRouter(prefix="/api/v1")
    router.include_router(social_auth.router, prefix="/auth/social")
    router.include_router(auth.router, prefix="/auth")
    router.include_router(movie.router, prefix="/movie")
    router.include_router(backlog.router, prefix="/backlog")
    app.include_router(router)
