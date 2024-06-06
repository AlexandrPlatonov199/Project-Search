import datetime
import typing
import uuid

import fastapi
import jwt
import pydantic
from pydantic import ValidationError

from app.pkg import models

__all__ = ["JWTService"]


class JWTService:
    """
    Сервис для работы с JWT (JSON Web Tokens).

    Args:
        access_token_public_key (str): Публичный ключ для access токенов.
        access_token_private_key (str): Приватный ключ для access токенов.
        refresh_token_public_key (str): Публичный ключ для refresh токенов.
        refresh_token_private_key (str): Приватный ключ для refresh токенов.
        access_token_expires (datetime.timedelta): Время жизни access токена.
        refresh_token_expires (datetime.timedelta): Время жизни refresh токена.
    """

    def __init__(
            self,
            access_token_public_key: str,
            access_token_private_key: str,
            refresh_token_public_key: str,
            refresh_token_private_key: str,
            access_token_expires: datetime.timedelta,
            refresh_token_expires: datetime.timedelta,
    ) -> None:
        self.access_token_public_key: str = access_token_public_key
        self.access_token_private_key: str = access_token_private_key
        self.refresh_token_public_key: str = refresh_token_public_key
        self.refresh_token_private_key: str = refresh_token_private_key
        self.access_token_expires: datetime.timedelta = access_token_expires
        self.refresh_token_expires: datetime.timedelta = refresh_token_expires

    @property
    def access_token_expires_utc(self) -> datetime.datetime:
        """Возвращает время истечения срока действия access токена в формате UTC."""
        return datetime.datetime.utcnow() + self.access_token_expires

    @property
    def refresh_token_expires_utc(self) -> datetime.datetime:
        """Возвращает время истечения срока действия refresh токена в формате UTC."""
        return datetime.datetime.utcnow() + self.refresh_token_expires

    def issue_access_token(
            self,
            user_id: uuid.UUID,
            is_activated: bool,
    ) -> str:
        """
        Генерирует access токен для пользователя.

        Args:
            user_id (uuid.UUID): ID пользователя.
            is_activated (bool): Статус активации пользователя.

        Returns:
            str: Сгенерированный access токен.
        """
        return jwt.encode(
            {
                "user_id": str(user_id),
                "is_activated": is_activated,
                "exp": datetime.datetime.now() + self.access_token_expires,
            },
            self.access_token_private_key,
            algorithm="RS256",
        )

    def decode_access_token(
            self,
            access_token: str,
    ) -> typing.Optional[models.JWTData]:
        """
        Декодирует access токен.

        Args:
            access_token (str): Access токен.

        Returns:
            typing.Optional[models.JWTData]: Данные JWT, если декодирование успешно, иначе None.
        """
        try:
            data = jwt.decode(
                access_token,
                self.access_token_public_key,
                algorithms=["RS256"],
                options={"require": ["user_id", "is_activated"]},
            )

            return pydantic.parse_obj_as(models.JWTData, data)
        except (jwt.PyJWTError, ValidationError):
            return None

    def issue_refresh_token(
            self,
            user_id: uuid.UUID,
            is_activated: bool,
    ) -> str:
        """
        Генерирует refresh токен для пользователя.

        Args:
            user_id (uuid.UUID): ID пользователя.
            is_activated (bool): Статус активации пользователя.

        Returns:
            str: Сгенерированный refresh токен.
        """
        return jwt.encode(
            {
                "user_id": str(user_id),
                "is_activated": is_activated,
                "exp": datetime.datetime.now() + self.refresh_token_expires,
            },
            self.refresh_token_private_key,
            algorithm="RS256",
        )

    def decode_refresh_token(
            self,
            refresh_token: str,
    ) -> typing.Optional[models.JWTData]:
        """
        Декодирует refresh токен.

        Args:
            refresh_token (str): Refresh токен.

        Returns:
            typing.Optional[models.JWTData]: Данные JWT, если декодирование успешно, иначе None.
        """
        try:
            data = jwt.decode(
                refresh_token,
                self.refresh_token_public_key,
                algorithms=["RS256"],
                options={"require": ["user_id", "is_activated"]},
            )
            return pydantic.parse_obj_as(models.JWTData, data)
        except (jwt.PyJWTError, ValidationError):
            return None

    def set_cookie(
            self,
            response: fastapi.Response,
            name: str,
            value: str,
            expires: datetime
    ) -> fastapi.Response:
        """
        Устанавливает cookie в ответе.

        Args:
            response (fastapi.Response): HTTP-ответ.
            name (str): Имя cookie.
            value (str): Значение cookie.
            expires (datetime): Время истечения срока действия cookie.

        Returns:
            fastapi.Response: Обновленный HTTP-ответ.
        """
        response.set_cookie(
            key=name,
            value=value,
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            path="/",
            secure=True,
            httponly=True,
            samesite="strict",
        )
        return response

    def generate_authorize_response(
            self,
            user,
            response: fastapi.Response
    ) -> models.AuthorizeUser:
        """
        Генерирует ответ авторизации, устанавливая access и refresh токены в cookie.

        Args:
            user: Пользователь.
            response (fastapi.Response): HTTP-ответ.

        Returns:
            models.AuthorizeUser: Объект с данными авторизации пользователя.
        """
        access_token = self.issue_access_token(user.id, is_activated=self.activate(user.is_activated))
        refresh_token = self.issue_refresh_token(user.id, is_activated=self.activate(user.is_activated))

        self.set_cookie(
            response=response,
            name="access_token",
            value=access_token,
            expires=self.access_token_expires_utc
        )
        self.set_cookie(
            response=response,
            name="refresh_token",
            value=refresh_token,
            expires=self.refresh_token_expires_utc
        )

        return models.AuthorizeUser(
            email=user.email,
            password=user.password,
            is_activated=user.is_activated,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    def activate(is_activated) -> bool:
        """
        Активирует пользователя.

        Args:
            is_activated: Статус активации пользователя.

        Returns:
            bool: True, если пользователь активирован.
        """
        is_activated = True
        return is_activated

    async def get_jwt_data(
            self,
            response: fastapi.Response,
            access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
            refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
            access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
    ) -> typing.Optional[models.JWTData]:
        """
        Извлекает данные JWT из токенов в заголовках или cookie.

        Args:
            response (fastapi.Response): HTTP-ответ.
            access_token_from_cookie (typing.Optional[str]): Access токен из cookie.
            refresh_token_from_cookie (typing.Optional[str]): Refresh токен из cookie.
            access_token_from_header (typing.Optional[str]): Access токен из заголовка.

        Returns:
            typing.Optional[models.JWTData]: Данные JWT, если декодирование успешно, иначе None.
        """
        access_token, refresh_token = None, None

        if access_token_from_header is not None and access_token_from_header.startswith("Bearer "):
            access_token = access_token_from_header.lstrip("Bearer").strip()
        if access_token is None:
            access_token = access_token_from_cookie
        if refresh_token is None:
            refresh_token = refresh_token_from_cookie

        jwt_data = None
        if access_token is not None:
            jwt_data = self.decode_access_token(access_token)
        if jwt_data is None:
            if refresh_token is None:
                return None
            jwt_data = self.decode_refresh_token(refresh_token)
            if jwt_data is None:
                return None
            # Обновить access_token и refresh_token
            new_access_token = self.issue_access_token(
                user_id=jwt_data.user_id,
                is_activated=jwt_data.is_activated,
            )
            new_refresh_token = self.issue_refresh_token(
                user_id=jwt_data.user_id,
                is_activated=jwt_data.is_activated,
            )
            self.set_cookie(
                response=response,
                name="access_token",
                value=new_access_token,
                expires=self.access_token_expires_utc
            )
            self.set_cookie(
                response=response,
                name="refresh_token",
                value=new_refresh_token,
                expires=self.refresh_token_expires_utc
            )
        return jwt_data
