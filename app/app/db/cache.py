import aioredis
import sys

REDIS_URL = "redis://localhost"


class Client():
    _client: aioredis.Redis = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    async def instance(cls) -> aioredis.Redis:
        if cls._client is not None:
            return cls._client

        try:
            client = aioredis.from_url(
                REDIS_URL, decode_responses=True, max_connections=10
            )

            if await client.ping():
                cls._client = client

                return client

        except aioredis.ConnectionError:
            print("Error occured during connect to Redis.")
            sys.exit(1)

        except aioredis.AuthenticationError:
            print("Authentication failed during connect to Redis.")
            sys.exit(1)


def cacheByStr(keygen, fn):
    async def wrapper(*args, **kwargs):
        key = keygen(*args, **kwargs)

        client = await Client.instance()

        if await client.exists(key):
            return await client.get(key)

        data = await fn(*args, **kwargs)

        await client.set(key, data)

        return data

    return wrapper


def cacheByHash(keygen, fn):
    async def wrapper(*args, **kwargs):
        key = keygen(*args, **kwargs)

        client = await Client.instance()

        if await client.exists(key):
            return await client.hget(key)

        data = await fn(*args, **kwargs)

        await client.hmset(key, data)

        return data

    return wrapper
