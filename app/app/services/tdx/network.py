import httpx
import time

from wsgiref.handlers import format_date_time
from hmac import digest
from hashlib import sha1
from base64 import b64encode

from config import settings

HOST = settings.TDX_HOST
API_ID = settings.TDX_API_ID
API_KEY = settings.TDX_API_KEY


def signature(date: str, key: str):
    return b64encode(
        digest(key=bytes(key, "utf-8"),
               msg=bytes(f'x-date: {date}', "utf-8"),
               digest=sha1)).decode()


def hmac(username: str, signature: str):
    return "hmac " + ",".join(
        list(
            map(
                lambda x: f'{x[0]}="{x[1]}"', {
                    'username': username,
                    'algorithm': 'hmac-sha1',
                    'headers': 'x-date',
                    'signature': signature
                }.items())))


async def GET(url: str):
    current_time = format_date_time(time.time())

    headers = {
        'Authorization':
        hmac(username=API_ID, signature=signature(current_time, API_KEY)),
        'x-date':
        current_time,
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(HOST + url, headers=headers)

        if res.status_code != 200:
            raise ConnectionError(
                f"GET {url} from TDX failed with {res.status_code}")

        return res
