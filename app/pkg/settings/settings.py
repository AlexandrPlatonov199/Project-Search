"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import urllib.parse
from typing import Optional
from functools import lru_cache

from pydantic import PostgresDsn, root_validator
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr


__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.
    """

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True
        #: bool: case-sensitive for env variables.
        case_sensitive = True
        #: str: delimiter for nested env variables.
        env_nested_delimiter = "__"


class Postgresql(_Settings):
    """Postgres settings."""

    HOST: str = "localhost"

    PORT: PositiveInt = 5432

    USER: str = "postgres"

    PASSWORD: SecretStr = SecretStr("postgres")

    DATABASE_NAME: str = "test"

    DSN: Optional[str] = None

    MIN_CONNECTION: PositiveInt = 1

    MAX_CONNECTION: PositiveInt = 16

    @root_validator(pre=True)
    def build_dsn(cls, values: dict):  # pylint: disable=no-self-argument
        """Build DSN for postgresql.

        Args:
            values: dict with all settings.

        Returns:
            dict with all settings and DSN.
        """

        values["DSN"] = PostgresDsn.build(
            scheme="postgresql",
            user=f"{values.get('USER')}",
            password=f"{urllib.parse.quote_plus(values.get('PASSWORD'))}",
            host=f"{values.get('HOST')}",
            port=f"{values.get('PORT')}",
            path=f"/{values.get('DATABASE_NAME')}",
        )
        return values


class APIServer(_Settings):
    """API settings."""

    INSTANCE_APP_NAME: str = "project_name"

    HOST: str = "localhost"

    PORT: PositiveInt = 5000


class Settings(_Settings):
    """Server settings."""

    API: APIServer

    POSTGRES: Postgresql


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
