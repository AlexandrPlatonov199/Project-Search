from fastapi import Depends
from starlette import status
from dependency_injector.wiring import inject, Provide

from app.internal.routes import profile_router
from app.internal.services import ProfileService, Services
from app.pkg import models


@profile_router.post(
    status_code=status.HTTP_201_CREATED,
    description="Create profile for user."

)
@inject
async def create_profile(
        cmd: models.CreateProfileCommand,
        profile_service: ProfileService = Depends(Provide[Services.user_service])
):
    return await profile_service.create_profile(cmd=cmd)
