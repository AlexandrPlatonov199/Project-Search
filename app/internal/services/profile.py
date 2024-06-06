"""Модуль для обработки профилей пользователей."""

import typing

import fastapi
from fastapi import HTTPException
from starlette import status

from app.internal.repository.repository import BaseRepository
from app.pkg import models

__all__ = ["ProfileService"]


class ProfileService:
    """
    Сервис для работы с профилями пользователей.

    Args:
        profile_repository (BaseRepository): Репозиторий профилей пользователей.
        jwt_service: Сервис JWT.
    """

    def __init__(
        self,
        profile_repository: BaseRepository,
        jwt_service,
    ):
        self.repository = profile_repository
        self.jwt_service = jwt_service

    async def create_profile(
        self,
        response: fastapi.Response,
        cmd: models.CreateProfileCommand,
        access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
    ) -> models.Profile:
        """
        Создает профиль пользователя.

        Args:
            response (fastapi.Response): HTTP-ответ.
            cmd (models.CreateProfileCommand): Данные для создания профиля.
            access_token_from_cookie (typing.Optional[str], optional): Access токен из cookie. Defaults to None.
            refresh_token_from_cookie (typing.Optional[str], optional): Refresh токен из cookie. Defaults to None.
            access_token_from_header (typing.Optional[str], optional): Access токен из заголовка. Defaults to None.

        Returns:
            models.Profile: Созданный профиль пользователя.
        """
        user = await self.jwt_service.get_jwt_data(
            response=response,
            access_token_from_cookie=access_token_from_cookie,
            refresh_token_from_cookie=refresh_token_from_cookie,
            access_token_from_header=access_token_from_header,
        )

        #TODO Добавить кастомные ошибки
        if user is not None and user.user_id == cmd.user_id:
            return await self.repository.create(cmd=cmd)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    async def read_profile(
        self,
        response: fastapi.Response,
        query: models.ReadProfileQuery,
        access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
        refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
        access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
    ):
        """
        Читает профиль пользователя.

        Args:
            response (fastapi.Response): HTTP-ответ.
            query (models.ReadProfileQuery): Запрос на чтение профиля.
            access_token_from_cookie (typing.Optional[str], optional): Access токен из cookie. Defaults to None.
            refresh_token_from_cookie (typing.Optional[str], optional): Refresh токен из cookie. Defaults to None.
            access_token_from_header (typing.Optional[str], optional): Access токен из заголовка. Defaults to None.

        Returns:
            [type]: [description]
        """
        user = await self.jwt_service.get_jwt_data(
            response=response,
            access_token_from_cookie=access_token_from_cookie,
            refresh_token_from_cookie=refresh_token_from_cookie,
            access_token_from_header=access_token_from_header,
        )

        if user is not None and user.user_id == query.user_id:
            return await self.repository.read(query=query)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    async def update_profile(
            self,
            response: fastapi.Response,
            cmd: models.UpdateProfileCommand,
            access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
            refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
            access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
    ):
        user = await self.jwt_service.get_jwt_data(
            response=response,
            access_token_from_cookie=access_token_from_cookie,
            refresh_token_from_cookie=refresh_token_from_cookie,
            access_token_from_header=access_token_from_header,
        )

        if user is not None and user.user_id == cmd.user_id:
            return await self.repository.update(cmd=cmd)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    async def delete_profile(
            self,
            response: fastapi.Response,
            cmd: models.DeleteProfileCommand,
            access_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="access_token"),
            refresh_token_from_cookie: typing.Optional[str] = fastapi.Cookie(None, alias="refresh_token"),
            access_token_from_header: typing.Optional[str] = fastapi.Header(None, alias="Authorization"),
    ):
        user = await self.jwt_service.get_jwt_data(
            response=response,
            access_token_from_cookie=access_token_from_cookie,
            refresh_token_from_cookie=refresh_token_from_cookie,
            access_token_from_header=access_token_from_header,
        )

        if user is not None and user.user_id == cmd.user_id:
            return await self.repository.delete(cmd=cmd)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

