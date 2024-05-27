"""Routes for user module."""
import uuid
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.routes import user_router
from app.internal.services import Services
from app.internal.services.users import UserService
from app.pkg import models
from app.pkg.models.exceptions import users


@user_router.get(
    "/{user_idL:uuid.UUID}}/",
    response_model=models.User,
    status_code=status.HTTP_200_OK,
    description="Get User",
)
@inject
async def read_user(
    user_id: uuid.UUID,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.read_user(
        query=models.ReadUserQuery(id=user_id),
    )


@user_router.post(
    "/",
    response_model=models.User,
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    responses={
        **users.UserNotFound.generate_openapi(),
        **users.TelegramUsernameAlreadyExists.generate_openapi(),
    },
)
@inject
async def create_city(
    cmd: models.CreateUserCommand,
    user_service: UserService = Depends(Provide[Services.user_service]),
):
    return await user_service.create_user(cmd=cmd)

