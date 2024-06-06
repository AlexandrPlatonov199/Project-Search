import fastapi

from app.internal.repository.postgresql import users
from app.pkg import models

__all__ = ["AuthService"]


class AuthService:
    """
    Сервис для аутентификации и авторизации пользователей.

    Args:
        user_repository (UserRepository): Репозиторий для взаимодействия с пользователями.
        jwt_service (JWTService): Сервис для работы с JWT токенами.
    """

    user_repository: users.UserRepository

    def __init__(
        self,
        user_repository,
        jwt_service,
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def sign_up_user(
        self, response: fastapi.Response, cmd: models.AuthorizeUserCommand
    ) -> models.AuthorizeUser:
        """
        Регистрирует нового пользователя и генерирует авторизационный ответ с JWT токенами.

        Args:
            response (fastapi.Response): HTTP-ответ.
            cmd (models.AuthorizeUserCommand): Команда с данными пользователя для регистрации.

        Returns:
            models.AuthorizeUser: Данные авторизованного пользователя с JWT токенами.
        """
        user = await self.user_repository.create(cmd=cmd)
        return self.jwt_service.generate_authorize_response(
            user=user,
            response=response,
        )

    async def sign_in_user(
        self, response: fastapi.Response, cmd: models.AuthorizeUserCommand
    ) -> models.AuthorizeUser:
        """
        Авторизует пользователя и генерирует авторизационный ответ с JWT токенами.

        Args:
            response (fastapi.Response): HTTP-ответ.
            cmd (models.AuthorizeUserCommand): Команда с данными пользователя для авторизации.

        Returns:
            models.AuthorizeUser: Данные авторизованного пользователя с JWT токенами.
        """
        user = await self.user_repository.read_email_password(cmd=cmd)
        return self.jwt_service.generate_authorize_response(
            user=user,
            response=response,
        )
