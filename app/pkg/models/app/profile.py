import typing
import uuid

from pydantic import PositiveInt
from pydantic.fields import Field

from app.pkg.models.base import BaseModel

__all__ = [
    "CreateProfileCommand",
    "Profile",
           ]


class ProfileBade(BaseModel):
    """Базовая модель профиля"""


class ProfileField:
    id: PositiveInt = Field()
    user_id: uuid.UUID = Field()
    first_name: typing.Optional[str] = Field(
        description="Имя пользователя.",
        example="Alexandr",
        default=None,
    )
    last_name: typing.Optional[str] = Field(
        description="Фамилия пользователя.",
        example="Popov",
        default=None,
    )
    telegram: typing.Optional[str] = Field(
        description="Телеграм пользователя.",
        example="@tester1337",
        default=None,
        regex=r"^@[\w\d_]{5,}$",
    )
    bio: typing.Optional[str] = Field(
        description="Биография пользователя.",
        default=None,
        example="Легко приспосабливаюсь к новым условиям и требованиям,"
                " что помогает мне быстро реагировать на изменения в"
                " процессе разработки."
    )


class _Profile(BaseModel):
    user_id: uuid.UUID = ProfileField.user_id
    first_name: typing.Optional[str] = ProfileField.first_name
    last_name: typing.Optional[str] = ProfileField.last_name
    telegram: typing.Optional[str] = ProfileField.telegram
    bio: typing.Optional[str] = ProfileField.bio


class Profile(_Profile):
    id: PositiveInt = ProfileField.id


class CreateProfileCommand(_Profile):
    ...

