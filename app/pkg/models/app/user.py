"""Models of user object."""
import typing
import uuid

from pydantic import EmailStr
from pydantic.fields import Field

from app.pkg.models.base import BaseModel

__all__ = [
    "User",
    "ReadUserQuery",
    "AuthorizeUserCommand",
    "ReadUserEmailQuery",
    "AuthorizeUser",
]


class BaseUser(BaseModel):
    """Base model for user."""


class UserFields:
    """
    Поля модели пользователя.

    Attributes:
        id (uuid.UUID): Идентификатор пользователя.
        email (typing.Optional[EmailStr]): Емаил пользователя.
        password (str): Пароль пользователя.
        is_activated (bool): Статус активации пользователя.
    """

    id: uuid.UUID = Field()
    email: typing.Optional[EmailStr] = Field(
        description="Емаил пользователя.",
        example="test@example.ru",
        default=None,
    )
    password: str = Field(
        description="Пароль пользователя",
        example="P@ssw0rd!",
        regex=r"^[\w\(\)\[\]\{\}\^\$\+\*@#%!&]{8,}$",
    )
    is_activated: bool = Field(description="Is activated.", example=False)


class _User(BaseUser):
    email: typing.Optional[EmailStr] = UserFields.email
    password: str = UserFields.password
    is_activated: bool = UserFields.is_activated


class User(_User):
    id: uuid.UUID = UserFields.id


class ReadUserQuery(BaseUser):
    id: uuid.UUID = UserFields.id


class ReadUserEmailQuery(BaseUser):
    email: typing.Optional[EmailStr] = UserFields.email


# Commands.
class AuthorizeUserCommand(BaseUser):
    email: typing.Optional[EmailStr] = UserFields.email
    password: str = UserFields.password


class AuthorizeUser(_User):
    access_token: str
    refresh_token: str
