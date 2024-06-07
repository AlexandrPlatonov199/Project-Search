"""Package resource's module.

All resources should be inherited from :class:`.BaseAsyncResource`.
"""

from abc import abstractmethod
from typing import TypeVar

from dependency_injector import resources

__all__ = ["BaseAsyncResource"]


_T = TypeVar("_T")


class BaseAsyncResource(resources.AsyncResource):
    """Abstract base class for async resources."""

    @abstractmethod
    async def init(self, *args, **kwargs) -> _T:
        """Getting connection.

        Args:
            *args: Positional arguments for ``get_connect`` method.
            **kwargs: Keyword arguments for ``get_connect`` method.
        """

    @abstractmethod
    async def shutdown(self, resource: _T):
        """Close connection.

        Args:
            resource: Resource returned by :meth:`BaseAsyncResource.init()` method.

        Notes:
            You should implement ``close`` method of your connector here.
        """
