import typing
import uuid

import fastapi
from fastapi import Depends
from starlette import status
from dependency_injector.wiring import inject, Provide

from app.internal.routes import profile_router
from app.internal.services import ProfileService, Services
from app.pkg import models


@profile_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create profile for user."

)
@inject
async def create_profile(
        response: fastapi.Response,
        cmd: models.CreateProfileCommand,
        profile_service: ProfileService = Depends(Provide[Services.profile_service]),
        access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),

):
    return await profile_service.create_profile(
        response=response,
        cmd=cmd,
        access_token_from_cookie=access_token_from_cookie,
        refresh_token_from_cookie=refresh_token_from_cookie,
        access_token_from_header=access_token_from_header,

    )


@profile_router.get(
    "/{user_id:uuid}",
    status_code=status.HTTP_200_OK,
    description="Get profile user.",
)
@inject
async def read_profile(
        response: fastapi.Response,
        user_id: uuid.UUID,
        profile_service: ProfileService = Depends(Provide[Services.profile_service]),
        access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),

):
    return await profile_service.read_profile(
        query=models.ReadProfileQuery(user_id=user_id),
        response=response,
        access_token_from_cookie=access_token_from_cookie,
        refresh_token_from_cookie=refresh_token_from_cookie,
        access_token_from_header=access_token_from_header,
    )


@profile_router.put(
    "/",
    status_code=status.HTTP_200_OK,
    description="Update profile user."
)
@inject
async def update_profile(
        response: fastapi.Response,
        cmd: models.UpdateProfileCommand,
        profile_service: ProfileService = Depends(Provide[Services.profile_service]),
        access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
):
    return await profile_service.update_profile(
        cmd=cmd,
        response=response,
        access_token_from_cookie=access_token_from_cookie,
        refresh_token_from_cookie=refresh_token_from_cookie,
        access_token_from_header=access_token_from_header,
    )
