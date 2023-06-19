from __future__ import annotations

import json

from typing import Union

from core.config import api_settings, app_settings, logging_settings
import httpx

from utils.logger import get_logger
from utils.tmdb_utils import (
    authenticate,
    get_popular_tv,
    get_request_token,
    retrieve_token,
    test_key,
)

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from core.db import Base, create_base_metadata, get_engine, get_session
from domain.schemas.tmdb import tmdb_media_schemas, tmdb_responses
from lib.constants import auth_endpoint, movie_endpoint, token_endpoint
from utils.time_utils import benchmark

engine = get_engine(connection="db/demo.sqlite", echo=True)
SessionLocal = get_session(engine=engine)
create_base_metadata(base_obj=Base, engine=engine)


def main():
    # log.debug(f"App settings: {app_settings}")
    # log.debug(f"API settings: {api_settings}")

    log.info("Testing API key")

    if not test_key():
        raise ValueError(f"Unable to validate API key.")

    _auth = authenticate(api_settings.API_READ_KEY)
    log.debug(f"Auth response: {_auth}")

    _token = get_request_token()
    # log.debug(f"Token: {_token}")

    token = retrieve_token(_token.text)
    log.debug(f"Token: {token}")

    log.info(f"Getting popular TV shows")
    popular_tv = get_popular_tv()

    pop_tv_dict: dict = popular_tv.text_json()

    # for k in pop_tv_dict.keys():
    #     log.debug(
    #         f"\nKey: {k}\nType: {type(pop_tv_dict[k])}\nValue: {pop_tv_dict[k]}\nPydantic schema line: {k}: {type(pop_tv_dict[k]).__name__} = Field(default=None)"
    #     )

    pop_tv: tmdb_media_schemas.MediaResponse = (
        tmdb_media_schemas.MediaResponse.parse_obj(pop_tv_dict)
    )

    log.debug(f"Popular TV: {pop_tv}")

    log.info(
        f"Found {pop_tv.total_results} popular TV shows. Results in {pop_tv.total_pages} pages."
    )

    pop_tv_shows: list[tmdb_media_schemas.TVShow] = []

    for tv_show in pop_tv.results:
        pop_tv_show: tmdb_media_schemas.TVShow = tmdb_media_schemas.TVShow.parse_obj(
            tv_show
        )

        pop_tv_shows.append(pop_tv_show)

    log.debug(f"Popular TV Shows: {pop_tv_shows}")
    log.debug(f"Found [{len(pop_tv_shows)}] popular TV shows")


if __name__ == "__main__":
    log.info("Starting app")
    with benchmark("Run main() function"):
        main()
    log.info("Finished.")
