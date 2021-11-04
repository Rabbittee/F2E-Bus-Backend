import os
import sys
from aioredis import BlockingConnectionPool, Redis, ConnectionError, AuthenticationError

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost")

pool = BlockingConnectionPool.from_url(REDIS_URL,
                                       decode_responses=True,
                                       max_connections=10)


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
