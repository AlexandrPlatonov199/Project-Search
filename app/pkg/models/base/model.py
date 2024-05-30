"""Base model for all models in API server."""

from __future__ import annotations

import time
import typing
from datetime import date, datetime
from typing import Any, Dict, List, Tuple, TypeVar
from uuid import UUID

import pydantic
from pydantic import UUID4
from jsf import JSF


__all__ = ["BaseModel", "Model"]

from app.pkg.models import types

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

    def migrate(
        self,
        model: type[BaseModel],
        random_fill: bool = False,
        match_keys: dict[str, str] | None = None,
        extra_fields: dict[str, typing.Any] | None = None,
    ) -> Model:
        """Migrate one model to another ignoring missmatch.

        Args:
            model:
                Heir BaseModel object.
            random_fill:
                If True, then the fields that are not in the
                model will be filled with random values.
            match_keys:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the names of the fields of the current model.
                Key: name of field in self-model.
                Value: name of field in a target model.
            extra_fields:
                The keys of this object are the names of the
                fields of the model to which the migration will be made, and the
                values are the values of the fields of the current model.

                Key: name of field in a target model.

                Value: value of field in a target model.

        Returns:
            pydantic model parsed from ``model``.
        """

        self_dict_model = self.to_dict(show_secrets=True)

        if not match_keys:
            match_keys = {}
        if not extra_fields:
            extra_fields = {}

        for key, value in match_keys.items():
            self_dict_model[key] = self_dict_model.pop(value)

        for key, value in extra_fields.items():
            self_dict_model[key] = value

        if not random_fill:
            return pydantic.parse_obj_as(model, self_dict_model)

        faker = JSF(model.schema()).generate()
        faker.update(self_dict_model)
        return pydantic.parse_obj_as(model, faker)

    class Config:
        """Pydantic config class.

        See Also:
            https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        # Use enum values instead of names.
        use_enum_values = True

        # Specify custom json encoders.
        json_encoders = {
            pydantic.SecretStr: lambda v: v.get_secret_value() if v else None,
            pydantic.SecretBytes: lambda v: v.get_secret_value() if v else None,
            types.EncryptedSecretBytes: lambda v: v.get_secret_value() if v else None,
            bytes: lambda v: v.decode() if v else None,
            datetime: lambda v: int(v.timestamp()) if v else None,
            date: lambda v: int(time.mktime(v.timetuple())) if v else None,
        }

        # Allow creating new fields in model.
        allow_population_by_field_name = True

        # Allow validate assignment.
        validate_assignment = True

        # Remove trailing whitespace
        anystr_strip_whitespace = True
