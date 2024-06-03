"""
Генераторы для моделей.

Этот модуль предоставляет фикстуры для генерации тестовых данных моделей с использованием библиотеки JSF.
"""

from typing import Any, Callable, Type
import pydantic
import pytest
from jsf import JSF
from app.pkg import models
from app.pkg.models.base import Model


def __generator(model: Type[Model], **kwargs) -> Callable[..., Model]:
    """
    Внутренняя функция для создания генератора тестовых данных для модели.

    Аргументы:
        model (Type[Model]): Тип модели, для которой создается генератор.
        **kwargs: Дополнительные параметры, которые будут добавлены к сгенерированным данным.

    Возвращает:
        Callable[..., Model]: Функция, которая при вызове генерирует экземпляр модели с тестовыми данными.
    """
    mock = JSF(model.schema())

    def generate() -> Any:
        """
        Генерирует тестовые данные для модели, обновляя их с учетом переданных параметров.

        Возвращает:
            Any: Экземпляр модели с тестовыми данными.
        """
        mock_generate = mock.generate()
        mock_generate.update(kwargs)
        return pydantic.parse_obj_as(model, mock_generate)

    return generate()


@pytest.fixture()
def user_generator() -> Callable[[], Any]:
    """
    Pytest фикстура для генерации тестовых данных модели User.

    Возвращает:
        Callable[[], Any]: Функция, которая генерирует экземпляр модели User с тестовыми данными.
    """
    return lambda **kwargs: __generator(models.User, **kwargs)
