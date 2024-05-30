"""Repository for user."""

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["UserRepository"]


class UserRepository(Repository):
    """User repository implementation."""
    @collect_response
    async def create(self, cmd: models.CreateUserCommand) -> models.User:
        q = """
            insert into users(
                email, telegram, first_name, last_name
            ) values (
                %(email)s, %(telegram)s, %(first_name)s, %(last_name)s
            )
            returning id, email, telegram, first_name, last_name
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadUserQuery) -> models.User:
        q = """
            select
                id, email, telegram, first_name, last_name
            from users
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()
