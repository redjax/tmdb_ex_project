from __future__ import annotations

import json

from core.config import APISettings, api_settings, app_settings, logging_settings
import httpx

from lib.constants import (
    auth_endpoint,
    base_url,
    get_logger,
    movie_endpoint,
    popular_tv_endpoint,
    session_endpoint,
    token_endpoint,
    tv_endpoint,
)
import pytest
import pytest_vcr
from utils.tmdb_utils import (
    get_popular_tv,
    get_request_token,
    retrieve_token,
    tmdb_media_schemas,
    tmdb_responses,
)

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)


## Set API key as a fixture
@pytest.fixture
def supply_api_key() -> str:
    api_key = api_settings.API_READ_KEY

    return api_key


def supply_auth_headers() -> dict[str, str]:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_settings.API_READ_KEY}",
    }

    return headers


def test_api_settings(api_settings: APISettings = api_settings):
    assert api_settings, "Missing api_settings"
    assert isinstance(
        api_settings, APISettings
    ), "api_settings must be of type APISettings"
    assert api_settings.API_READ_KEY, "Missing API_READ_KEY"


@pytest.mark.live_api
@pytest.mark.vcr()
def test_api_auth(headers: dict = supply_auth_headers()):
    url = f"{api_settings.BASE_URL}/{auth_endpoint}"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            assert (
                res.status_code == 200
            ), f"Non-200 response code returned: [{res.status_code}: {res.reason_phrase}]: {res.text}"

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


@pytest.mark.xfail(reason="Known bad endpoint.")
@pytest.mark.vcr()
def test_fail_api_auth(headers: dict = supply_auth_headers()):
    url = f"{api_settings.BASE_URL}/{auth_endpoint}/bad"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            assert (
                res.status_code == 200
            ), f"Non-200 response code returned: [{res.status_code}: {res.reason_phrase}]: {res.text}"

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


@pytest.mark.live_api
@pytest.mark.vcr()
def test_retrieve_api_token(headers: dict = supply_auth_headers()):
    url = f"{api_settings.BASE_URL}/{auth_endpoint}/{token_endpoint}/new"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            assert (
                res.status_code == 200
            ), f"Non-200 response code returned: [{res.status_code}: {res.reason_phrase}]: {res.text}"

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )
