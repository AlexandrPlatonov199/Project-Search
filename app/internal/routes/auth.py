"""Routes for auth module."""
import typing

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.routes import auth_router
from app.internal.services import Services
from app.internal.services.auth import AuthService
from app.internal.services.jwt import JWTService
from app.pkg import models


@auth_router.post(
    "/signup/",
    status_code=status.HTTP_201_CREATED,
    response_model=models.AuthorizeUser,
)
@inject
async def sign_up(
        response: fastapi.Response,
        cmd: models.AuthorizeUserCommand,
        auth_service: AuthService = Depends(Provide[Services.auth_service]),
):
    return await auth_service.sign_up_user(
        response,
        cmd=cmd,
    )


@auth_router.post(
    "/sign_in/",
    status_code=status.HTTP_200_OK
)
@inject
async def sign_in(
        response: fastapi.Response,
        cmd: models.AuthorizeUserCommand,
        auth_service: AuthService = Depends(Provide[Services.auth_service]),
):

    return await auth_service.sign_in_user(
        response=response,
        cmd=cmd,
    )


@auth_router.delete(
    "/logout/",
)
async def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


# @auth_router.get(
#     "/check/",
#     status_code=status.HTTP_200_OK
# )
# @inject
# async def check(
#         jwt_service: JWTService = Depends(JWTService.get_jwt_data),
# ):
#     return jwt_service

