"""Service for manage user."""

from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["UserService"]

from app.pkg.models.exceptions.users import UserNotFound


class UserService:
    """Service for managing user."""

    def __init__(self, user_repository: BaseRepository):
        """
        Initialize UserService.

        Args:
            user_repository (BaseRepository): Repository for user.
        """
        self.repository = user_repository

    async def create_user(self, cmd: models.CreateUserCommand) -> models.User:
        """Create user.

        Args:
            cmd: CreateUserCommand command.

        Returns:
            User: Created user.
        """
        return await self.repository.create(cmd=cmd)

    async def read_user(self, query: models.ReadUserQuery) -> models.User:
        """Read user.

        Args:
            query: ReadUserQuery query.

        Returns:
            User: Read user.
        """

        return await self.repository.read(query=query)

