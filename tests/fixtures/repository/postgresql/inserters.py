"""Inserters для репозитория PostgreSQL.

Этот модуль содержит фикстуры для вставки моделей в базу данных с использованием генераторов JSF.
"""


from typing import Type

import pytest

from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model


async def __inserter(
    repository: Repository,
    generator,
    cmd_model: Type[Model],
    **kwargs,
) -> tuple[Model, Model]:
    """Вставляет общую модель в базу данных.

    Аргументы:
        repository (Repository): Экземпляр репозитория.
        generator (Callable[..., Model]): Генератор модели.
        cmd_model (Type[Model]): Модель команды.
        **kwargs: Поля модели.

    Возвращает:
        tuple[Model, Model]: Кортеж с результатом вставки и командой.
    """

    cmd = generator(**kwargs).migrate(model=cmd_model)

    return await repository.create(cmd=cmd), cmd


@pytest.fixture()
async def user_inserter(user_repositories, user_generator):
    """Вставляет пользователя в базу данных."""

    return lambda **kwargs: __inserter(
        repository=user_repositories,
        generator=user_generator,
        cmd_model=models.CreateUserCommand,
        **kwargs,
    )
