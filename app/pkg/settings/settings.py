"""Модуль для загрузки настроек из `.env` или, если сервер запущен с параметром `dev`, из `.env.dev`."""

import datetime
import pathlib
import urllib.parse
from functools import lru_cache
from typing import Optional

from dotenv import find_dotenv
from pydantic import PostgresDsn, root_validator, validator
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

from app.pkg.models.core.logger import LoggerLevel
from app.pkg.utils.generate_rsa_keys import generate_rsa_keys

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Базовые настройки для всех настроек.

    Используйте двойное подчеркивание для вложенных переменных среды.
    """

    class Config:
        """Конфигурация настроек."""

        #: str: Кодировка файла окружения.
        env_file_encoding = "utf-8"
        #: str: Разрешить пользовательские поля в модели.
        arbitrary_types_allowed = True
        #: bool: Регистрозависимость для переменных среды.
        case_sensitive = True
        #: str: Разделитель для вложенных переменных среды.
        env_nested_delimiter = "__"


class Postgresql(_Settings):
    """Настройки для работы с PostgreSQL."""

    HOST: str = "localhost"
    PORT: PositiveInt = 5432
    USER: str = "postgres"
    PASSWORD: SecretStr = SecretStr("postgres")
    DATABASE_NAME: str = "test"
    DSN: Optional[str] = None
    MIN_CONNECTION: PositiveInt = 1
    MAX_CONNECTION: PositiveInt = 16

    @root_validator(pre=True)
    def build_dsn(cls, values: dict):
        """Создает строку подключения к PostgreSQL."""

        values["DSN"] = PostgresDsn.build(
            scheme="postgresql",
            user=f"{values.get('USER')}",
            password=f"{urllib.parse.quote_plus(values.get('PASSWORD'))}",
            host=f"{values.get('HOST')}",
            port=f"{values.get('PORT')}",
            path=f"/{values.get('DATABASE_NAME')}",
        )
        return values


class Logging(_Settings):
    """Настройки логирования."""

    LEVEL: LoggerLevel = LoggerLevel.DEBUG
    FOLDER_PATH: pathlib.Path = pathlib.Path("./src/logs")

    @validator("FOLDER_PATH")
    def __create_dir_if_not_exist(cls, v: pathlib.Path):
        """Создает каталог, если его не существует."""

        if not v.exists():
            v.mkdir(exist_ok=True, parents=True)
        return v


class APIServer(_Settings):
    """Настройки API."""

    INSTANCE_APP_NAME: str = "project_name"
    HOST: str = "localhost"
    PORT: PositiveInt = 5000
    LOGGER: Logging


class Jwt(_Settings):
    """Настройки JWT."""

    ACCESS_TOKEN_PRIVATE_KEY: Optional[str] = None
    ACCESS_TOKEN_PUBLIC_KEY: Optional[str] = None
    REFRESH_TOKEN_PRIVATE_KEY: Optional[str] = None
    REFRESH_TOKEN_PUBLIC_KEY: Optional[str] = None
    ACCESS_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(minutes=5)
    REFRESH_TOKEN_EXPIRES: datetime.timedelta = datetime.timedelta(days=30)

    @root_validator(pre=True)
    def gen_rsa_keys(cls, values: dict):
        """Генерирует пары ключей RSA."""

        public_key_access, private_key_access = generate_rsa_keys()
        public_key_refresh, private_key_refresh = generate_rsa_keys()

        values["ACCESS_TOKEN_PRIVATE_KEY"] = private_key_access
        values["ACCESS_TOKEN_PUBLIC_KEY"] = public_key_access
        values["REFRESH_TOKEN_PRIVATE_KEY"] = private_key_refresh
        values["REFRESH_TOKEN_PUBLIC_KEY"] = public_key_refresh
        return values


class Settings(_Settings):
    """Настройки сервера."""

    API: APIServer
    POSTGRES: Postgresql
    JWT: Jwt


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Создает экземпляр настроек."""

    return Settings(_env_file=find_dotenv(env_file))
