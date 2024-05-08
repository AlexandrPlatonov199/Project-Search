"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import typing
from functools import lru_cache

from pydantic import RedisDsn, root_validator
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


class APIServer(_Settings):
    """API settings."""

    INSTANCE_APP_NAME: str = "project_name"

    HOST: str = "localhost"

    PORT: PositiveInt = 5000


class Settings(_Settings):
    """Server settings."""

    API: APIServer



@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
