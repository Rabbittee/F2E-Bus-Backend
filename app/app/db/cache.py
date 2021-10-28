from aioredis import BlockingConnectionPool, Redis, ConnectionError, AuthenticationError
import sys

REDIS_URL = "redis://localhost"

pool = BlockingConnectionPool.from_url(
    REDIS_URL,
    decode_responses=True,
    max_connections=10
)


async def connection() -> Redis:
    try:
        client = Redis(connection_pool=pool)

        if await client.ping():
            return client

    except ConnectionError:
        print("Error occured during connect to Redis.")
        sys.exit(1)

    except AuthenticationError:
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
