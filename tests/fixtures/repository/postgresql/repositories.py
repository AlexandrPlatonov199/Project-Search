"""All fixtures for postgresql repositories."""

import pytest

from app.internal.repository.postgresql import UserRepository


@pytest.fixture()
async def user_repositories() -> UserRepository:
    return UserRepository()
