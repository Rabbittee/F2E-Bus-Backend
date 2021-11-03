import os
import sys
from aioredis import BlockingConnectionPool, Redis, ConnectionError, AuthenticationError

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost")
REDIS_URL = 'redis://:pb3361052f6a0bdbd5bc124d1b5a523514e7a5757d47847c5d61d575af6299d4b@ec2-50-19-118-165.compute-1.amazonaws.com:24369'

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
