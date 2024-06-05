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
    id: uuid.UUID = Field()
    email: typing.Optional[EmailStr] = Field(
        description="User email.",
        example="test@example.ru",
        default=None,
    )
    telegram: typing.Optional[str] = Field(
        description="Telegram user.",
        example="@tester1337",
        default=None,
        regex=r"^@[\w\d_]{5,}$",
    )
    first_name: typing.Optional[str] = Field(
        description="First name user.",
        example="Alexandr",
        default=None,
    )
    password: str = Field(
        description="Password user",
        example="P@ssw0rd!",
        regex=r"^[\w\(\)\[\]\{\}\^\$\+\*@#%!&]{8,}$"
    )
    last_name: typing.Optional[str] = Field(
        description="Last name user.",
        example="Popov",
        default=None,
    )
    is_activated: bool = Field(description="Is activated.", example=False)
    has_avatar: bool = Field(description="Has avatar", example=False)
    about: typing.Optional[str] = Field(
        description="About user.",
        default=None,
    )


class _User(BaseUser):
    email: typing.Optional[EmailStr] = UserFields.email
    password: str = UserFields.password
    telegram: typing.Optional[str] = UserFields.telegram
    first_name: typing.Optional[str] = UserFields.first_name
    last_name: typing.Optional[str] = UserFields.last_name


class User(_User):
    id: uuid.UUID = UserFields.id
    is_activated: bool = UserFields.is_activated


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
