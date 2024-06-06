from app.internal.repository.repository import BaseRepository
from app.pkg import models


class ProfileService:
    def __init__(
            self,
            profile_repository: BaseRepository,
    ):
        self.repository = profile_repository

    async def create_profile(self, cmd: models.CreateProfileCommand) -> models.Profile:

        return await self.repository.create(cmd=cmd)
