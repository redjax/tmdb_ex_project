from __future__ import annotations

from datetime import datetime, timedelta
import json

from typing import Any, Optional, Union

from pydantic import BaseModel, Field, ValidationError, validator

# from lib.constants import ...

# from domain.schemas.tmdb.tmdb_responses import


class MediaGenres(BaseModel):
    """Class to store TMDB genres for media items.

    The genre dict is shared between different media types.
    """

    id: int = Field(default=None)
    name: str = Field(default=None)


class MovieCollection(BaseModel):
    id: int = Field(default=None)
    name: str = Field(default=None)
    poster_path: str = Field(default=None)
    backdrop_path: str = Field(default=None)


class ProductionCompanies(BaseModel):
    id: int = Field(default=None)
    logo_path: str = Field(default=None)
    name: str = Field(default=None)
    origin_country: str = Field(default=None)


class TVShowCreator(BaseModel):
    id: int = Field(default=None)
    credit_id: str = Field(default=None)
    name: str = Field(default=None)
    gender: int = Field(default=None)
    profile_path: str = Field(default=None)


class BaseMediaResponse(BaseModel):
    page: int = Field(default=None)
    results: list[MediaTVShow] = Field(default=None)
    total_pages: int = Field(default=None)
    total_results: int = Field(default=None)
    popularity: float = Field(default=None)


class BaseMedia(BaseModel):
    """Base media (tv-show, movie, etc) object.

    All media classes inherit common properties
    they share on TMDB (i.e. a name, a list of genres, etc)
    and functions from this base.
    """

    adult: bool = Field(default=None)
    backdrop_path: str = Field(default=None)
    genres: list[MediaGenres] = Field(default=None)
    genre_ids: list[int] = Field(default=None)
    overview: str = Field(default=None)
    popularity: float = Field(default=None)
    poster_path: str = Field(default=None)
    tmdb_id: int = Field(default=None, alias="id")
    original_language: str = Field(default=None)
    vote_average: float = Field(default=None)
    vote_count: int = Field(default=None)
    homepage: str = Field(default=None)
    production_companies: list[ProductionCompanies] = Field(default=None)
    runtime: int = Field(default=None)


class MediaTVShowAiredEpisode(BaseMedia):
    name: str = Field(default=None)
    air_date: str = Field(default=None)
    episode_number: int = Field(default=None)
    production_code: str = Field(default=None)
    season_number: int = Field(default=None)
    show_id: int = Field(default=None)
    still_path: str = Field(default=None)


class MediaTVShowNetwork(BaseModel):
    tmdb_id: int = Field(default=None, alias="id")
    logo_path: str = Field(default=None)
    name: str = Field(default=None)
    origin_country: str = Field(default=None)


class MediaTVShowSeason(BaseMedia):
    air_date: str = Field(default=None)
    episode_count: int = Field(default=None)
    name: str = Field(default=None)
    season_number: int = Field(default=None)


class MediaTVShow(BaseMedia):
    created_by: list[TVShowCreator] = Field(default=None)
    episode_run_time: list[int] = Field(default=None)
    first_air_date: str = Field(default=None)
    in_production: bool = Field(default=None)
    languages: list[str] = Field(default=None)
    last_air_date: str = Field(default=None)
    last_episode_to_air: MediaTVShowAiredEpisode = Field(default=None)
    next_episode_to_air: MediaTVShowAiredEpisode = Field(default=None)
    name: str = Field(default=None)
    origin_country: list = Field(default=None)
    original_language: str = Field(default=None)
    original_name: str = Field(default=None)
    episode_run_time: list[int] = Field(default=None)
    networks: list[MediaTVShowNetwork] = Field(default=None)
    number_of_episodes: int = Field(default=None)
    number_of_seasons: int = Field(default=None)
    seasons: list[MediaTVShowSeason] = Field(default=None)
    type: str = Field(default=None)


class MediaMovie(BaseMedia):
    belongs_to_collection: MovieCollection = Field(default=None)
    budget: int = Field(default=None)
    imdb_id: str = Field(default=None)
    original_title: str = Field(default=None)
    release_date: str = Field(default=None)
    revenue: int = Field(default=None)
    title: str = Field(default=None)
    video: bool = Field(default=None)


class MediaResponse(BaseMediaResponse):
    pass
