from uuid import uuid4

import pytest

from app.pkg import models
from app.pkg.models.exceptions.users import UserNotFound


@pytest.mark.postgresql
async def test_read(
        clean_postgres,
        user_repositories,
        user_inserter
):
    user, _ = await user_inserter()

    result = await user_repositories.read(query=user.migrate(models.ReadUserQuery))

    assert user == result


@pytest.mark.postgresql
async def test_not_found(
        clean_postgres,
        user_repositories,
        user_inserter
):
    user, _ = await user_inserter()

    query = user.migrate(model=models.ReadUserQuery, extra_fields={"id": uuid4()})

    with pytest.raises(UserNotFound):
        await user_repositories.read(query=query)
