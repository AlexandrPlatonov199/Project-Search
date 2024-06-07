"""Abstract repository interface."""

from abc import ABC
from typing import TypeVar

__all__ = ["Repository", "BaseRepository"]

BaseRepository = TypeVar("BaseRepository", bound="Repository")


class Repository(ABC):
    """Base repository interface.

    All repositories must implement this interface.

    Notes:
        All methods must be asynchronous.
    """

    async def create(self, cmd):
        """Create model.

        Args:
            cmd: Specific command for create model. Must be inherited from
                ``Model``.

        Returns:
            Type of the parent model.
        """
        raise NotImplementedError

    async def read(self, query):
        """Read model.

        Args:
            query: Specific query for read model. Must be inherited from
                ``Model``.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError

    async def read_all(self):
        """Read all rows."""

        raise NotImplementedError

    async def update(self, cmd):
        """Update model.

        Notes: In this method cmd must contain id of the model for update and ALL
        fields for update.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError

    async def delete(self, cmd):
        """Delete model.

        Notes: In this method you should mark row as deleted. You must not delete row
            from database.

        Returns:
            Type of the parent model.
        """

        raise NotImplementedError
