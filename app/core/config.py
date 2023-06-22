from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, BaseSettings, Field, ValidationError, validator

THIS_DIR = Path(__file__).parent

allowed_log_levels = ["DEBUG", "CRITICAL", "WARNING", "ERROR", "INFO"]


class AppSettings(BaseSettings):
    APP_TITLE: str = Field(default="Default App Title", env="APP_TITLE")
    APP_DESCRIPTION: str = Field(
        default="Default app description", env="APP_DESCRIPTION"
    )
    APP_VERSION: str = Field(default="0.0.1", env="APP_VERSION")

    class Config:
        env_file = f"{THIS_DIR}/env_files/.env"


class APISettings(BaseSettings):
    BASE_URL: str = Field(default=None, env="BASE_URL")
    API_KEY: str = Field(default=None, env="API_KEY")
    API_READ_KEY: str = Field(default=None, env="API_READ_KEY")

    class Config:
        env_file = f"{THIS_DIR}/env_files/api.env"


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    username: str = Field(default=None, env="REDIS_USERNAME")
    ## Hide password from repr, i.e. when printing an instance of this class.
    password: str = Field(default=None, env="REDIS_PASS", repr=False)

    class Config:
        env_file = f"{THIS_DIR}/env_files/db.env"


class LoggingSetting(BaseSettings):
    LOG_LEVEL: str = "INFO"

    @validator("LOG_LEVEL")
    def valid_log_level(cls, v) -> str:
        if not v:
            v = "INFO"

        if v not in allowed_log_levels:
            raise ValidationError(
                f"Invalid log level [{v}]. Must be one of {allowed_log_levels}"
            )

        return v

    class Config:
        env_file = f"{THIS_DIR}/env_files/logging.env"


app_settings = AppSettings()
logging_settings = LoggingSetting()
api_settings = APISettings()
redis_settings = RedisSettings()
