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
    async def create(self, cmd: models.AuthorizeUserCommand) -> models.User:
        q = """
            insert into users(
                email, password
            ) values (
                %(email)s, %(password)s
            )
            returning id, email, password, is_activated
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadUserQuery) -> models.User:
        q = """
            select
                id, email, password, is_activated
            from users
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_email_password(
        self, cmd: models.AuthorizeUserCommand
    ) -> models.User:
        q = """
            select
                id, email, password, is_activated
            from users
            where email = %(email)s
            and password = %(password)s
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
