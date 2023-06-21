from __future__ import annotations

import typing
import httpx
import redis

from core.config import logging_settings, redis_settings

from utils.logger import get_logger
from utils.uuid_utils import get_rand_uuid

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from utils.time_utils import benchmark

print(f"Redis settings: {redis_settings}")
## Create Redis client
client: redis.Redis = redis.Redis(
    host=redis_settings.host, port=redis_settings.port, password=redis_settings.password
)


if __name__ == "__main__":
    log.debug(f"Redis settings ({type(redis_settings)}): {redis_settings}")

    test_value = get_rand_uuid()

    log.debug(f"Set a value")
    ## Set value
    with benchmark(description=f"Set test-key value to: {test_value}"):
        try:
            client.set("test-key", test_value)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception setting value in Redis. Details: {exc}"
            )

    with benchmark(description=f"Get value of test-key"):
        ## Get value
        try:
            _v = client.get("test-key")
        except Exception as exc:
            raise Exception(
                f"Unhandled exception getting value from Redis. Details: {exc}"
            )

        log.info(f"Retrieved value ({type(_v).__name__}): {_v}")
        log.debug(f"Decoded ({type(_v.decode())}): {_v.decode()}")
