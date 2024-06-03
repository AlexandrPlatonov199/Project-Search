"""Автоматически обрезает все таблицы перед каждым тестом."""

import pytest

from app.internal.repository.postgresql import connection


async def __clean_postgres():
    """Обрезает все таблицы (кроме миграций yoyo) перед каждым тестом."""

    q = """
        CREATE OR REPLACE FUNCTION truncate_tables() RETURNS void AS $$
        DECLARE
            statements CURSOR FOR
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
                    AND tablename NOT LIKE '%yoyo%'
                    AND tablename NOT LIKE 'user_roles';
        BEGIN
            FOR stmt IN statements LOOP
                EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
    """

    async with connection.get_connection(return_pool=True) as pool:
        async with connection.acquire_connection(pool) as cursor:
            await cursor.execute(q)
            await cursor.execute("SELECT truncate_tables();")


@pytest.fixture()
async def clean_postgres():
    """Очищает postgres."""
    await __clean_postgres()
