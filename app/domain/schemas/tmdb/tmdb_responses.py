from __future__ import annotations

from datetime import datetime, timedelta
import json

from typing import Any, Optional, Union

from httpx import Response
from pydantic import BaseModel, Field, ValidationError, validator

class BaseHeaders(BaseModel):
    """Base response headers schema.

    Response Headers are an HTTPX class. Convert to Pydantic.
    """

    content_type: str = Field(default=None, alias="content-type")
    transfer_encoding: str = Field(default=None, alias="transfer-encoding")
    server: str = Field(default=None)
    content_encoding: str = Field(default=None, alias="content-encoding")
    date: str = Field(default=None)
    cache_control: str = Field(default=None, alias="cache-control")
    etag: str = Field(default=None)
    vary: str = Field(default=None)
    x_cache: str = Field(default=None, alias="x-cache")
    via: str = Field(default=None)
    x_amz_cf_pop: str = Field(default=None, alias="x-amz-cf-pop")
    alt_svc: str = Field(default=None, alias="alt-svc")
    x_amz_cf_id: str = Field(default=None, alias="x-amz-cf-id")


class BaseResponse(BaseModel):
    """Base response schema.

    Responses are an HTTPX class. Convert to Pydantic.
    """

    url: str = Field(default=None)
    headers: BaseHeaders = Field(default=None)
    status_code: int = Field(default=None)
    reason_phrase: str = Field(default=None)
    text: str = Field(default=None)
    content: bytes = Field(default=None)
    history: list = Field(default=None)
    is_client_error: bool = Field(default=None)
    is_server_error: bool = Field(default=None)
    is_redirect: bool = Field(default=None)
    is_error: bool = Field(default=None)
    is_success: bool = Field(default=None)
    is_informational: bool = Field(default=None)
    is_stream_consumed: bool = Field(default=None)
    original_response: Response = Field(default=None)

    @property
    def content_decode(self):
        _content = self.content

        try:
            _decode = _content.decode("utf-8")

            return _decode

        except Exception as exc:
            raise Exception(
                f"Unhandled exception decoding content bytes. Details: {exc}"
            )

    def text_json(self) -> dict:
        try:
            _text_json = json.loads(self.text)

            return _text_json
        except Exception as exc:
            raise Exception(
                f"Unhandled exception converting response text to JSON. Details: {exc}"
            )

    class Config:
        arbitrary_types_allowed = True


class ReqHeaders(BaseHeaders):
    """Inherit header properties from BaseHeaders."""

    pass


class ReqResponse(BaseResponse):
    """Inherit response properties from BaseResponse."""

    pass


class ReqToken(BaseModel):
    success: bool = Field(default=None)
    expires_at: str = Field(default=None)
    request_token: str = Field(default=None)
