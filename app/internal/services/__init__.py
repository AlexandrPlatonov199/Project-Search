"""Service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories, postgresql
from app.internal.services.auth import AuthService
from app.internal.services.profile import ProfileService
from app.pkg.settings import settings
from app.internal.services.jwt import JWTService
from app.internal.services.users import UserService


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    repositories: postgresql.Repositories = providers.Container(
        Repositories.postgres,
    )

    jwt_service = providers.Factory(
        JWTService,
        access_token_private_key=settings.JWT.ACCESS_TOKEN_PRIVATE_KEY,
        access_token_public_key=settings.JWT.ACCESS_TOKEN_PUBLIC_KEY,
        refresh_token_private_key=settings.JWT.REFRESH_TOKEN_PRIVATE_KEY,
        refresh_token_public_key=settings.JWT.REFRESH_TOKEN_PUBLIC_KEY,
        access_token_expires=settings.JWT.ACCESS_TOKEN_EXPIRES,
        refresh_token_expires=settings.JWT.REFRESH_TOKEN_EXPIRES,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=repositories.user_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=repositories.user_repository,
        jwt_service=jwt_service,
    )

    profile_service = providers.Factory(
        ProfileService,
        profile_repository=repositories.profile_repository,
    )
