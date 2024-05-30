"""Exceptions for a User model."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UserNotFound",
    "EmailAlreadyExists",
    "TelegramUsernameAlreadyExists",
]


class UserNotFound(BaseAPIException):
    message = "User not found."
    status_code = status.HTTP_404_NOT_FOUND


class EmailAlreadyExists(BaseAPIException):
    message = "This 'email' already exists."
    status_code = status.HTTP_409_CONFLICT


class TelegramUsernameAlreadyExists(BaseAPIException):
    message = "This 'telegram_username' already exists."
    status_code = status.HTTP_409_CONFLICT


__constrains__ = {
    "users_email_key": EmailAlreadyExists,
    "users_telegram_key": TelegramUsernameAlreadyExists,
}
