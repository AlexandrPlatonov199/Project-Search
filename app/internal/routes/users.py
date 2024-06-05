"""Routes for user module."""
import uuid

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app.internal.routes import user_router
from app.internal.services import Services
from app.internal.services.users import UserService
from app.pkg import models


@user_router.get(
    "/{user_id:uuid}/",
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
