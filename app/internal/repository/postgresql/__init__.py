"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.postgresql.profiles import ProfileRepository
from app.internal.repository.postgresql.users import UserRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    user_repository = providers.Factory(UserRepository)

    profile_repository = providers.Factory(ProfileRepository)
