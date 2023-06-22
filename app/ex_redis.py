"""https://redis.readthedocs.io/en/stable/examples.html."""
from __future__ import annotations

import json
import typing

from core.config import logging_settings, redis_settings
import redis

from redis.commands.json.path import Path as j_path
from redis.commands.search.field import NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from utils.logger import get_logger
from utils.uuid_utils import get_rand_uuid

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from utils.time_utils import benchmark

print(f"Redis settings: {redis_settings}")


def get_redis_creds(
    username: str = redis_settings.username,
    password: str = redis_settings.password,
) -> redis.UsernamePasswordCredentialProvider:
    """https://redis.readthedocs.io/en/stable/examples/connection_examples.html#Connecting-to-a-redis-instance-with-username-and-password-credential-provider."""
    try:
        credentials: redis.UsernamePasswordCredentialProvider = (
            redis.UsernamePasswordCredentialProvider(username, password)
        )
    except Exception as exc:
        raise Exception(
            f"Unhandled exception setting Redis credentials. Details: {exc}"
        )

    return credentials


## Create Redis client
redis_client: redis.Redis = redis.Redis(
    host=redis_settings.host,
    port=redis_settings.port,
    credential_provider=get_redis_creds(),
    decode_responses=True,
)


## Validator functions
def validate_redis_client(client: redis.Redis = None) -> redis.Redis:
    if not client:
        raise ValueError("Missing a Redis client")

    if not isinstance(client, redis.Redis):
        raise ValueError("Client must be of type redis.Redis")

    return client


def validate_redis_key(key: str = None) -> str:
    if not key:
        raise ValueError("Missing a lookup key")

    if not isinstance(key, str):
        raise ValueError("Redis keys must be strings")

    return key


def validate_redis_val(val: str = None) -> str:
    allowed_val_types: list[typing.Type] = [str, dict]

    if not val:
        raise ValueError("Missing a value")

    if not isinstance(val, str):
        if not isinstance(val, dict):
            raise ValueError(
                f"Invalid type for Redis key's value: {type(val)}. Must be one of {allowed_val_types}"
            )

    return val


def validate_redis_expire(expire: int = None, none_ok: bool = True) -> int:
    if not expire:
        if not none_ok:
            raise ValueError("Missing int value for expire")
        else:
            pass

    if not isinstance(expire, int):
        if not none_ok:
            raise ValueError("Invalid type for expire, must be int")
        else:
            if expire is None:
                pass

    return expire


def ping_redis(client: redis.Redis = None):
    validate_redis_client(client)

    try:
        client.ping()
    except Exception as exc:
        raise Exception(f"Unhandled exception pinging Redis instance. Details: {exc}")


def key_exists(key: str = None, client: redis.Redis = None) -> bool:
    validate_redis_client(client)
    validate_redis_key(key)

    try:
        ## Check if key exists. Returns 1 if True, 0 if False
        _exists = client.exists(key)

        if _exists == 1:
            return True
        elif _exists == 0:
            return False
        else:
            raise Exception(
                f"Unexpected value returned while checking for existence of key {key}: {_exists}."
            )

    except Exception as exc:
        log.error(
            Exception(
                f"Unhandled error retrieving value of key [{key}]. Details: {exc}"
            )
        )

        return False


def set_val(
    key: str = None,
    val: typing.Union[str, dict] = None,
    client: redis.Redis = None,
    update: bool = True,
    expire: int = None,
):
    validate_redis_client(client=client)
    validate_redis_key(key=key)
    validate_redis_val(val=val)
    validate_redis_expire(expire=expire)

    def set_str_val(c: redis.Redis = client, v: str = val, k: str = key):
        c.set(k, v)

    def set_dict_val(c: redis.Redis = client, v: str = val):
        c.mset(v)

    try:
        if not key_exists(client=client, key=key):
            if not expire:
                log.debug(f"Setting value of {key} to {val}")
                # client.set(key, val)
                if isinstance(val, str):
                    set_str_val()
                elif isinstance(val, dict):
                    set_dict_val(val)
            else:
                log.debug(
                    f"Setting value of {key} to {val}. Will expire in {expire} seconds"
                )
                client.setex(key, expire, val)

        else:
            if update:
                if not expire:
                    log.debug(f"Updating value of {key} to {val}")
                    client.set(key, val)
                else:
                    log.debug(
                        f"Updating value of {key} to {val}. Setting expiration of {expire} seconds"
                    )
                    client.setex(key, expire, val)
            else:
                return f"Key {key} already exists. Skipping update."

    except Exception as exc:
        raise Exception(
            f"Unhandled exception setting Redis key [{key}] to value {val}. Details: {exc}"
        )


def set_expire(key: str = None, expire: int = 0, client: redis.Redis = None):
    validate_redis_client(client=client)
    validate_redis_key(key=key)
    validate_redis_expire(expire=expire)

    try:
        client.expire(name=key, time=expire)

    except Exception as exc:
        raise Exception(
            f"Unhandled exception setting expiration of {expire} seconds on key {key}. Details: {exc}"
        )


def get_val(key: str = None, client: redis.Redis = None):
    validate_redis_client(client)
    validate_redis_key(key)

    try:
        if key_exists(key=key, client=client):
            val = client.get(key)

        else:
            return False

    except Exception as exc:
        raise Exception(
            f"Unhandled error retrieving value of key [{key}]. Details: {exc}"
        )

    return val


def get_ttl(key: str = None, client: redis.Redis = None) -> int:
    validate_redis_key(key)
    validate_redis_client(client)

    try:
        _ttl: int = client.ttl(key)

        return _ttl

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting time-to-live for key [{key}]. Details: {exc}"
        )


if __name__ == "__main__":
    test_key = get_val(client=redis_client, key="test-key")
    log.debug(f"Test ({type(test_key)}): {test_key}")

    test_nonexistant = get_val(client=redis_client, key="none")
    log.debug(f"Test non-existant (should be False): {test_nonexistant}")

    test_set = set_val(
        client=redis_client, key="test-set", val=get_rand_uuid(), update=False
    )

    ## Set a key that will expire
    test_expire = set_val(
        client=redis_client, key="test-expire", val="I will expire!", expire=5
    )
    log.debug(f"Test expire: {test_expire}")

    ## Set a new key, then set an expiration
    temp_key = set_val(
        client=redis_client, key="test-expire2", val="I will also expire!"
    )
    set_expire(key="test-expire2", expire=10, client=redis_client)

    ## Get the TTL for a key with an expiration
    expire_key_ttl = get_ttl(client=redis_client, key="test-expire2")
    log.debug(f"TTL for key test-expire2: {expire_key_ttl}")

    ## Get the TTL for a key without an expiration
    non_expire_key_ttl = get_ttl(client=redis_client, key="test-set")
    log.debug(f"TTL for non-expiring key test-set: {non_expire_key_ttl}")

    ## Set a dict as a value
    ex_dict = {
        "employee_name": "Adam Adams",
        "employee_age": 30,
        "position": "Software Engineer",
    }

    # dict_val = set_val(key="test-dict", val=ex_dict, client=redis_client)
