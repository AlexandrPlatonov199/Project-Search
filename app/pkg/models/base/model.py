"""Base model for all models in API server."""

from __future__ import annotations

import time
import typing
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import UUID

import pydantic
from pydantic import UUID4


__all__ = ["BaseModel", "Model"]

Model = TypeVar("Model", bound="BaseModel")
_T = TypeVar("_T")


class BaseModel(pydantic.BaseModel):
    """Base model for all models in API server."""

    def to_dict(
        self,
        show_secrets: bool = False,
        values: dict[Any, Any] = None,
        **kwargs,
    ) -> dict[Any, Any]:
        """Make a representation model from a class object to Dict object.

        Args:
            show_secrets:
                bool.
                default False.
                Shows secret in dict an object if True.
            values:
                Using an object to write to a Dict object.
            **kwargs:
                Optional arguments to be passed to the Dict object.

        Raises:
            TypeError: If ``values`` are not a Dict object.

        Returns:
            Dict object with reveal password filed.
        """

        values = self.dict(**kwargs).items() if not values else values.items()
        r = {}
        for k, v in values:
            v = self.__cast_values(v=v, show_secrets=show_secrets)
            r[k] = v
        return r

    def __cast_values(self, v: _T, show_secrets: bool, **kwargs) -> _T:
        """Cast value for dict object.

        Args:
            v:
                Any value.
            show_secrets:
                If True, then the secret will be revealed.

        Warnings:
            This method is not memory optimized.
        """

        if isinstance(v, (List, Tuple)):
            return [
                self.__cast_values(v=ve, show_secrets=show_secrets, **kwargs)
                for ve in v
            ]

        elif isinstance(v, (pydantic.SecretBytes, pydantic.SecretStr)):
            return self.__cast_secret(v=v, show_secrets=show_secrets)

        elif isinstance(v, Dict) and v:
            return self.to_dict(show_secrets=show_secrets, values=v, **kwargs)

        elif isinstance(v, (UUID, UUID4)):
            return str(v)

        elif isinstance(v, datetime):
            return v.timestamp()

        return v

    @staticmethod
    def __cast_secret(v, show_secrets: bool) -> str:
        """Cast secret value to str.

        Args:
            v: pydantic.Secret* object.
            show_secrets: bool value. If True, then the secret will be revealed.

        Returns: str value of ``v``.
        """

        if isinstance(v, pydantic.SecretBytes):
            return v.get_secret_value().decode() if show_secrets else str(v)
        elif isinstance(v, pydantic.SecretStr):
            return v.get_secret_value() if show_secrets else str(v)
