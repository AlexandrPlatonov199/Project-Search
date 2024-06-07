"""Конфигурация для pytest."""

import asyncio


import pytest

from app.configuration import __containers__
from app.pkg.connectors import PostgresSQL



# Список плагинов pytest.
pytest_plugins = [
    "tests.fixtures.repository.postgresql.repositories",
    "tests.fixtures.repository.postgresql.postgresql",
    "tests.fixtures.repository.postgresql.inserters",
    "tests.fixtures.router.client",
    "tests.fixtures.router.endpoints",
    "tests.fixtures.router.responses",
    "tests.fixtures.models.controller",
    "tests.fixtures.models.generators",
    "tests.fixtures.handlers.equals",
    "tests.fixtures.settings",
    # Путь к модулю с фикстурами.
]

# Метка pytest для использования anyio.
pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def event_loop(request):
    """Создает экземпляр основного цикла событий для каждого теста.

    Примечания:
        Эта фикстура используется для anyio тестов.

    Предупреждения:
        Полная изоляция для каждого теста гарантируется только в том случае,
        если тесты выполняются последовательно.
    """

    _ = request
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_sessionstart(session):
    _ = session

    # Устанавливаем окружение контейнеров для тестирования.
    __containers__.set_environment(
        connectors=[PostgresSQL],
        pkg_name="tests",
        testing=True,
    )
