from __future__ import annotations

import json
import random

from typing import Union

from core.config import api_settings, logging_settings
import httpx

from utils.logger import get_logger

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from domain.schemas.tmdb import tmdb_media_schemas, tmdb_responses
from lib.constants import (
    auth_endpoint,
    basic_auth_headers,
    popular_tv_endpoint,
    session_endpoint,
    token_endpoint,
    tv_endpoint,
    valid_media_types,
)
from utils.file_utils import check_file_exist

def authenticate(
    headers: dict = basic_auth_headers,
) -> tmdb_responses.ReqResponse:
    """Make authentication request.

    https://developer.themoviedb.org/docs/authentication-application
    """
    url = f"{api_settings.BASE_URL}/{auth_endpoint}"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            auth_dict = {
                "url": str(res.url),
                "headers": res.headers,
                "status_code": res.status_code,
                "reason_phrase": res.reason_phrase,
                "text": res.text,
                "content": res.content,
                "history": res.history,
                "is_client_error": res.is_client_error,
                "is_server_error": res.is_server_error,
                "is_redirect": res.is_redirect,
                "is_error": res.is_error,
                "is_success": res.is_success,
                "is_informational": res.is_informational,
                "is_stream_consumed": res.is_stream_consumed,
                "original_response": res,
            }

            _auth: tmdb_responses.ReqResponse = tmdb_responses.ReqResponse.parse_obj(
                auth_dict
            )

            # log.debug(f"Auth: {_auth}")

            if not res.status_code == 200:
                log.error(
                    f"Non-200 response [{res.status_code}: {res.reason_phrase}]: {res.text}"
                )

            return _auth

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


def get_request_token(
    headers: dict = basic_auth_headers,
) -> tmdb_responses.ReqResponse:
    """Request a token for session verification.

    After authentication, a token can be generated. This token can
    be used for authentication during the script's operations, and
    can be passed into a session.
    """
    url = f"{api_settings.BASE_URL}/{auth_endpoint}/{token_endpoint}/new"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            token_dict = {
                "url": str(res.url),
                "headers": res.headers,
                "status_code": res.status_code,
                "reason_phrase": res.reason_phrase,
                "text": res.text,
                "content": res.content,
                "history": res.history,
                "is_client_error": res.is_client_error,
                "is_server_error": res.is_server_error,
                "is_redirect": res.is_redirect,
                "is_error": res.is_error,
                "is_success": res.is_success,
                "is_informational": res.is_informational,
                "is_stream_consumed": res.is_stream_consumed,
                "original_response": res,
            }

            _token: tmdb_responses.ReqResponse = tmdb_responses.ReqResponse.parse_obj(
                token_dict
            )

            if not res.status_code == 200:
                log.error(
                    f"Non-200 response [{res.status_code}: {res.reason_phrase}]: {_token.text}"
                )

            # log.debug(f"Token: {_token}")

            return _token

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


def retrieve_token(token_dict: Union[str, dict[str, Union[bool, str]]] = None):
    if not token_dict:
        raise ValueError("Missing token dict")

    if not isinstance(token_dict, dict):
        try:
            token_dict: dict[str, Union[bool, str]] = json.loads(token_dict)

        except Exception as exc:
            raise Exception(
                f"Unhandled exception converting token_dict to dict. Details: {exc}"
            )

    token = tmdb_responses.ReqToken.parse_obj(token_dict)

    return token


def test_key(headers: dict = basic_auth_headers) -> bool:
    url = f"{api_settings.BASE_URL}/{auth_endpoint}"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            valid_token_dict = {
                "url": str(res.url),
                "headers": res.headers,
                "status_code": res.status_code,
                "reason_phrase": res.reason_phrase,
                "text": res.text,
                "content": res.content,
                "history": res.history,
                "is_client_error": res.is_client_error,
                "is_server_error": res.is_server_error,
                "is_redirect": res.is_redirect,
                "is_error": res.is_error,
                "is_success": res.is_success,
                "is_informational": res.is_informational,
                "is_stream_consumed": res.is_stream_consumed,
                "original_response": res,
            }

            valid_token: tmdb_responses.ReqResponse = (
                tmdb_responses.ReqResponse.parse_obj(valid_token_dict)
            )

            # log.debug(f"Valid token: {valid_token.text}")

            if not res.status_code == 200:
                log.error(
                    f"Non-200 response [{res.status_code}: {res.reason_phrase}]: {res.text}"
                )

            valid = json.loads(res.text)

            if valid["status_code"] == 1:
                log.info(f"API token is valid")
                return True
            else:
                log.error(
                    f"Unabled to validate API key. Reason: {valid_token.reason_phrase}"
                )
                return False

            # log.debug(f"Valid key: {_token}")

            # return _token

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


def get_popular_tv(headers: dict = basic_auth_headers, page: int = 1):
    if not isinstance(page, int):
        if isinstance(page, str):
            page = int(page)

        if not page:
            page = 1

        raise ValueError("Page must be an int")

    url = f"{api_settings.BASE_URL}/{tv_endpoint}/{popular_tv_endpoint}&page={page}"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            popular_tv_dict = {
                "url": str(res.url),
                "headers": res.headers,
                "status_code": res.status_code,
                "reason_phrase": res.reason_phrase,
                "text": res.text,
                "content": res.content,
                "history": res.history,
                "is_client_error": res.is_client_error,
                "is_server_error": res.is_server_error,
                "is_redirect": res.is_redirect,
                "is_error": res.is_error,
                "is_success": res.is_success,
                "is_informational": res.is_informational,
                "is_stream_consumed": res.is_stream_consumed,
                "original_response": res,
            }

            popular_tv: tmdb_responses.ReqResponse = (
                tmdb_responses.ReqResponse.parse_obj(popular_tv_dict)
            )

            # log.debug(f"Popular TV ({type(popular_tv)}): {popular_tv}")

            if not res.status_code == 200:
                log.error(
                    f"Non-200 response [{res.status_code}: {res.reason_phrase}]: {res.text}"
                )

            return popular_tv

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


def get_tv_episode(headers: dict = basic_auth_headers, tmdb_id: int = None):
    if not tmdb_id:
        raise ValueError("Missing TMDB ID")

    if not isinstance(tmdb_id, int):
        tmdb_id = int(tmdb_id)

    url = f"https://api.themoviedb.org/3/tv/{tmdb_id}"

    log.info(f"Requesting {url}")

    try:
        with httpx.Client() as client:
            res = client.get(url, headers=headers)

            popular_tv_dict = {
                "url": str(res.url),
                "headers": res.headers,
                "status_code": res.status_code,
                "reason_phrase": res.reason_phrase,
                "text": res.text,
                "content": res.content,
                "history": res.history,
                "is_client_error": res.is_client_error,
                "is_server_error": res.is_server_error,
                "is_redirect": res.is_redirect,
                "is_error": res.is_error,
                "is_success": res.is_success,
                "is_informational": res.is_informational,
                "is_stream_consumed": res.is_stream_consumed,
                "original_response": res,
            }

            popular_tv: tmdb_responses.ReqResponse = (
                tmdb_responses.ReqResponse.parse_obj(popular_tv_dict)
            )

            # log.debug(f"Popular TV ({type(popular_tv)}): {popular_tv}")

            if not res.status_code == 200:
                log.error(
                    f"Non-200 response [{res.status_code}: {res.reason_phrase}]: {res.text}"
                )

            return popular_tv

    except Exception as exc:
        raise Exception(
            f"Unhandled exception making authentication request. Details: {exc}"
        )


def get_bad_ids(bad_id_file: str = "bad_ids") -> list[int]:
    """Read bad IDs from a file."""
    known_bad_ids: list[int] = []

    check_file_exist(_file=bad_id_file)

    try:
        with open(bad_id_file, "r+") as read_f:
            lines = read_f.read()

            for line in lines:
                known_bad_ids.append(line)

    except Exception as exc:
        raise Exception(
            f"Unhandled exception reading bad IDs from {bad_id_file}. Details: {exc}"
        )

    return known_bad_ids


def append_bad_id(bad_id: int = None, bad_id_file: str = "bad_ids"):
    """Append a known bad ID to a file/list."""
    if not isinstance(bad_id, str):
        bad_id = str(bad_id)

    check_file_exist(_file=bad_id_file)

    try:
        bad_ids = get_bad_ids(bad_id_file=bad_id_file)

        # display(f"Bad IDs: {bad_ids}")

        if bad_id not in bad_ids:
            try:
                with open(bad_id_file, "a+") as out_file:
                    out_file.write(f"{bad_id}\n")

            except Exception as exc:
                raise Exception(
                    f"Unhandled exception appending bad ID [{bad_id}] to file {bad_id_file}. Details: {exc}"
                )

    except Exception as exc:
        raise Exception(
            f"Unhandled exception opening file {bad_id_file}. Details: {exc}"
        )


def check_bad_id(_id: Union[int, str] = None, bad_id_file: str = None) -> bool:
    if not _id:
        raise ValueError("Missing ID to check.")

    if not isinstance(_id, str):
        _id = str(_id)

    if not bad_id_file:
        raise ValueError("Missing file with known bad IDs.")

    if not check_file_exist(_file=bad_id_file):
        raise ValueError(f"File does not exist: {bad_id_file}")

    # display(f"Bad ID file: {bad_id_file}")

    with open(bad_id_file, "r+") as read_f:
        lines = read_f.readlines()

        if _id in lines:
            return False

        return True


def generate_rand_id(type: str = None, floor: int = 1, ceiling: int = 1000) -> int:
    if not type:
        raise ValueError(f"Missing media type. Must be one of {valid_media_types}")

    if type not in valid_media_types:
        raise ValueError(
            f"Type [{type}] is not an accepted media type. Must be one of {valid_media_types}"
        )

    _id = random.randint(floor, ceiling)

    while not check_bad_id(_id, bad_id_file=f"bad_{type}_ids"):
        print(f"Encountered a known bad {type} ID: [{_id}]. Trying again.")

        _id = random.randint(1, 1000)

    return _id
