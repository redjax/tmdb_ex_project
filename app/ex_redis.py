from __future__ import annotations

import typing

from core.config import logging_settings, redis_settings
import httpx
import redis

from utils.logger import get_logger
from utils.uuid_utils import get_rand_uuid

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from utils.time_utils import benchmark

print(f"Redis settings: {redis_settings}")
## Create Redis client
client: redis.Redis = redis.Redis(
    host=redis_settings.host, port=redis_settings.port, password=redis_settings.password
)


def set_value(var: str = None, val=None, client: redis.Redis = client) -> bool:
    if not isinstance(var, str):
        raise ValueError(f"Var/key name must be a string")

    try:
        client.set(var, val)

        return True
    except Exception as exc:
        log.error(
            Exception(f"Unhandled exception setting value in Redis. Details: {exc}")
        )

        return False


def get_value(
    var: str = None, client: redis.Redis = client
) -> typing.Union[bytes, bool]:
    try:
        _v = client.get("test-key")

        return _v
    except Exception as exc:
        log.error(
            Exception(f"Unhandled exception getting value from Redis. Details: {exc}")
        )

        return False


if __name__ == "__main__":
    log.debug(f"Redis settings ({type(redis_settings)}): {redis_settings}")

    test_value = get_rand_uuid()

    log.info(f"Setting test-key")
    ## Set value
    with benchmark(description=f"Set test-key value to: {test_value}"):
        # try:
        #     client.set("test-key", test_value)
        # except Exception as exc:
        #     raise Exception(
        #         f"Unhandled exception setting value in Redis. Details: {exc}"
        #     )

        _set_v = set_value(var="test-key", val=test_value)

    test_dict: dict = {"key1": "var1", "key2": "var2"}

    log.info(f"Setting test-dict")
    with benchmark(description=f"Set test-dict value to: {test_dict}"):
        _set_dict = set_value(var="test-dict", val=test_dict)

    with benchmark(description=f"Get value of test-dict"):
        ## Get value
        # try:
        #     _v = client.get("test-key")
        # except Exception as exc:
        #     raise Exception(
        #         f"Unhandled exception getting value from Redis. Details: {exc}"
        #     )

        _v_dict = get_value(var="test-dict")

        log.info(f"Retrieved dict value ({type(_v_dict).__name__}): {_v_dict}")
        log.debug(f"Decoded ({type(_v_dict.decode())}): {_v_dict.decode()}")

    with benchmark(description=f"Get value of test-key"):
        _v = get_value(var="test-key")

        log.info(f"Retrieved value ({type(_v).__name__}): {_v}")
        log.debug(f"Decoded ({type(_v.decode())}): {_v.decode()}")
