"""Collect response from aiopg and convert it to an annotated model."""

from functools import wraps
from typing import List, Type, Union

import pydantic
from psycopg2.extras import RealDictRow

from app.internal.repository.postgresql.handlers.handle_exception import \
    handle_exception
from app.pkg.models.base import Model
from app.pkg.models.exceptions.repository import EmptyResult

__all__ = ["collect_response"]


def collect_response(fn):
    """Convert response from aiopg to an annotated model.

    Args:
        fn:
            Target function that contains a query in postgresql.

    Returns:
        The model that is specified in type hints of `fn`.

    Raises:
        EmptyResult: when a query of `fn` returns None.
    """

    @wraps(fn)
    @handle_exception
    async def inner(
        *args: object,
        **kwargs: object,
    ) -> Union[List[Type[Model]], Type[Model]]:
        """Inner function of :func:`.collect_response`. Convert response from
        aiopg to an annotated model.

        Args:
            *args:
                Positional arguments.
            **kwargs:
                Keyword arguments.

        Raises:
            EmptyResult: when a query of `fn` returns None.

        Returns:
            The model that is specified in type hints of `fn`.
        """

        response = await fn(*args, **kwargs)
        if not response:
            raise EmptyResult

        return pydantic.parse_obj_as(
            (ann := fn.__annotations__["return"]),
            await __convert_response(response=response, annotations=str(ann))
        )

    return inner


async def __convert_response(response: RealDictRow, annotations: str):
    """Converts the response of the request to List of models or to a single
    model.

    Args:
        response:
            Response of an aiopg query.
        annotations:
            Annotations of `fn`.

    Returns:
        List[`Model`] if List is specified in the type annotations,
        or a single `Model` if `Model` is specified in the type annotations.
    """

    r = response.copy()

    if annotations.replace("typing.", "").startswith("List"):
        return [await __convert_memory_viewer(item) for item in r]
    return await __convert_memory_viewer(r)


async def __convert_memory_viewer(r: RealDictRow):
    """Convert memory viewer in bytes.

    Notes:
        aiopg returns memory viewer in query response,
        when in database type of cell `bytes`.

    Returns:
        `RealDictRow` with converted memory viewer in bytes.
    """

    for key, value in r.items():
        if isinstance(value, memoryview):
            r[key] = value.tobytes()
    return r
