"""Service for manage user."""

from app.internal.repository.repository import BaseRepository
from app.pkg import models

__all__ = ["UserService"]


class UserService:
    """Service for managing user."""

    def __init__(
        self,
        user_repository: BaseRepository,
    ):
        """
        Initialize UserService.

        Args:
            user_repository (BaseRepository): Repository for user.
        """
        self.repository = user_repository

    async def read_user(self, query: models.ReadUserQuery) -> models.User:
        """Read user.

        Args:
            query: ReadUserQuery query.

        Returns:
            User: Read user.
        """
        print(f"query user_service {query}")

        return await self.repository.read(query=query)
