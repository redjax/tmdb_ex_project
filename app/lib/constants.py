from __future__ import annotations

from typing import Union

from core.config import api_settings, app_settings, logging_settings
from utils.logger import get_logger

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

default_req_cache_dir = ".cache"
default_serialize_dir = ".serialize"

base_url: str = api_settings.BASE_URL
api_key: str = api_settings.API_READ_KEY

movie_endpoint: str = "movie"
tv_endpoint: str = "tv"
auth_endpoint: str = "authentication"
token_endpoint: str = "token"
session_endpoint: str = "session"

popular_tv_endpoint: str = "popular?language=en-US"

basic_auth_headers: dict = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}",
}

valid_media_types: list[str] = ["movie", "tv"]
