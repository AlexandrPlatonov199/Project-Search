"""Module for testing create user command."""

from uuid import uuid4

import pytest

from app.pkg import models
from app.pkg.models.exceptions.users import TelegramUsernameAlreadyExists, EmailAlreadyExists


@pytest.mark.postgresql
async def test_create(clean_postgres, user_generator, user_repositories):

    _ = clean_postgres

    user = user_generator()

    cmd = user.migrate(model=models.CreateUserCommand)

    result = await user_repositories.create(cmd=cmd)

    assert result == user.migrate(
        model=models.User,
        extra_fields={"id": result.id}
    )


@pytest.mark.postgresql
async def test_unique_email(
        clean_postgres,
        user_generator,
        user_repositories,
        user_inserter,
):
    _ = clean_postgres

    user, _ = await user_inserter(
        email=f"{uuid4().hex}@example.com",
        telegram=None
    )

    cmd = user_generator(email=user.email).migrate(
        model=models.CreateUserCommand,
    )

    with pytest.raises(EmailAlreadyExists):
        await user_repositories.create(cmd=cmd)


@pytest.mark.postgresql
async def test_unique_telegram(
        clean_postgres,
        user_generator,
        user_repositories,
        user_inserter,
):

    _ = clean_postgres

    user, _ = await user_inserter(
        telegram=f"@{uuid4().hex}",
        email=None
    )
    cmd = user_generator(telegram=user.telegram).migrate(
        model=models.CreateUserCommand
    )

    with pytest.raises(TelegramUsernameAlreadyExists):
        await user_repositories.create(cmd=cmd)
