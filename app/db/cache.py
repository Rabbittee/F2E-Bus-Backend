import sys
from aioredis import from_url, Redis, ConnectionError, AuthenticationError

from app.config import settings


async def connection() -> Redis:
    try:
        client = from_url(settings.REDIS_URL, decode_responses=True)

        if await client.ping():
            return client

    except ConnectionError:
        print("Error occured during connect to Redis.")
        sys.exit(1)

    except AuthenticationError:
        print("Authentication failed during connect to Redis.")
        sys.exit(1)
