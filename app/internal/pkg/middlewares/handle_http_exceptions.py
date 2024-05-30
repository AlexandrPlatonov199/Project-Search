"""Handlers that handle internal error raise and returns ``http json``
response.
"""

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.pkg.logger import get_logger
from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.repository import DriverError

__all__ = [
    "handle_internal_exception",
    "handle_api_exceptions",
    "handle_drivers_exceptions",
]

logger = get_logger(__name__)


def handle_drivers_exceptions(request: Request, exc: DriverError):
    """Handle all internal exceptions of :class:`.DriverError`.

    Args:
        request:
            ``Request`` instance.
        exc:
            Exception inherited from :class:`.DriverError`.

    Returns:
        ``JSONResponse`` object with status code 500.
    """

    del request  # unused

    if exc.details:
        logger.error(msg=exc.details)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": exc.message},
    )


def handle_api_exceptions(request: Request, exc: BaseAPIException):
    """Handle all internal exceptions that inherited from
    :class:`.BaseAPIException`.

    Args:
        request:
            ``Request`` instance.
        exc:
            Exception inherited from :class:`.BaseAPIException`.

    Returns:
        ``JSONResponse`` object with status code from ``exc.status_code``.
    """

    del request  # unused

    logger.info(exc)

    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


def handle_internal_exception(request: Request, exc: Exception):
    """Handle all internal unhandled exceptions.

    Args:
        request:
            ``Request`` instance.
        exc:
            ``Exception`` instance.

    Returns:
        ``JSONResponse`` object with status code 500.
    """

    del request  # unused

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": repr(exc)},
    )
