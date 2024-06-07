"""Server configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configuration.events import on_shutdown, on_startup
from app.internal.pkg.middlewares.handle_http_exceptions import (
    handle_api_exceptions,
    handle_drivers_exceptions,
    handle_internal_exception,
)
from app.internal.routes import __routes__
from app.pkg.models.base import BaseAPIException
from app.pkg.models.types.fastapi import FastAPITypes
from app.pkg.settings import settings

__all__ = ["Server"]


class Server:
    """
    Регистрация всех необходимых требований для корректной работы экземпляра сервера.

    Attributes:
        __app (FastAPI): Экземпляр приложения ``FastAPI``.
        __app_name (str): Имя приложения, используемое для метрик Prometheus
         и логов Loki.
            Получено из :class:`.Settings`:attr:`.INSTANCE_APP_NAME`.
    """

    __app: FastAPI
    __app_name: str = settings.API.INSTANCE_APP_NAME

    def __init__(self, app: FastAPI):
        """
        Инициализирует экземпляр сервера и регистрирует все необходимые требования
        для корректной работы экземпляра сервера.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.
        """

        self.__app = app
        self._register_routes(app)
        self._register_events(app)
        self._register_middlewares(app)
        self._register_http_exceptions(app)

    def get_app(self) -> FastAPI:
        """
        Возвращает текущий экземпляр приложения.

        Returns:
            FastAPI: Экземпляр приложения ``FastAPI``.
        """
        return self.__app

    @staticmethod
    def _register_events(app: FastAPITypes.instance) -> None:
        """
        Регистрирует события :func:`.on_startup` и :func:`.on_shutdown`.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.

        Returns:
            None
        """

        app.on_event("startup")(on_startup)
        app.on_event("shutdown")(on_shutdown)

    @staticmethod
    def _register_routes(app: FastAPITypes.instance) -> None:
        """
        Включает роутеры в экземпляр ``FastAPI`` из ``__routes__``.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.

        Returns:
            None
        """

        __routes__.register_routes(app)

    @staticmethod
    def __register_cors_origins(app: FastAPITypes.instance) -> None:
        """
        Регистрирует CORS origins. В производственной среде следует использовать
         только доверенные origins.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.

        Returns:
            None
        """

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_middlewares(self, app: FastAPI) -> None:
        """
        Применяет middlewares для маршрутов.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.

        Returns:
            None
        """

        self.__register_cors_origins(app)

    @staticmethod
    def _register_http_exceptions(app: FastAPITypes.instance) -> None:
        """
        Регистрирует HTTP исключения.
        Экземпляр обрабатывает исключения ``BaseAPIException``,
        возникающие внутри функций.

        Args:
            app (FastAPI): Экземпляр приложения ``FastAPI``.

        Returns:
            None
        """

        app.add_exception_handler(BaseAPIException, handle_api_exceptions)
        app.add_exception_handler(BaseAPIException, handle_drivers_exceptions)
        app.add_exception_handler(BaseAPIException, handle_internal_exception)
