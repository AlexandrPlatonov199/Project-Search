from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import \
    collect_response
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["ProfileRepository"]


class ProfileRepository(Repository):

    @collect_response
    async def create(self, cmd: models.CreateProfileCommand) -> models.Profile:
        q = """
            insert into profiles(
                user_id, first_name, last_name, telegram, bio
                ) values (
                    %(user_id)s, %(first_name)s, %(last_name)s, %(telegram)s, %(bio)s
                )
                returning id, user_id, first_name, last_name, telegram, bio
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadProfileQuery) -> models.Profile:
        q = """
            select 
                id , user_id, first_name, last_name, telegram, bio
            from profiles
            where user_id = %(user_id)s
            """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all(self) -> List[models.Profile]:
        q = """
             select
                id , user_id, first_name, last_name, telegram, bio
            from profiles
            """
        async with get_connection() as cur:
            await cur.execute(q)
            return await cur.fetchall()

    @collect_response
    async def update(self, cmd: models.UpdateProfileCommand) -> models.Profile:
        q = """
            update profiles
            set
                first_name = %(first_name)s,
                last_name = %(last_name)s,
                bio = %(bio)s
            where user_id = %(user_id)s
            returning id, user_id, first_name, last_name, telegram, bio
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteProfileCommand) -> models.Profile:
        q = """
            delete from profiles
            where user_id = %(user_id)s
            returning id, user_id, first_name, last_name, telegram, bio
            """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
