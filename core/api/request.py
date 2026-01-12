import asyncio
from typing import Any, Literal

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientError,
    ContentTypeError,
    InvalidURL,
    ServerTimeoutError,
)
from aiohttp_client_cache import CachedSession, SQLiteBackend
from dotenv import load_dotenv

from config import Settings
from .errors import (
    APIError,
    BadRequestError,
    RateLimitError,
    UnexpectedStatusError,
)

load_dotenv()


voxyl_cache = SQLiteBackend(
    cache_name=".cache/voxyl",
    expire_after=300,
)

skin_cache = SQLiteBackend(
    cache_name=".cache/skin",
    expire_after=900,
)


class VoxylAPI:
    def __init__(self, api_key: str = Settings.API_KEY):
        self.base_url = Settings.BASE_URL
        self.api_key = api_key
        self.session = CachedSession(cache=voxyl_cache)

    async def close(self):
        await self.session.close()

    async def _make_request(
        self,
        session: ClientSession,
        endpoint: Any,
        **kwargs: Any,
    ) -> Any:
        url = f"{self.base_url}/{endpoint.value.format(**kwargs)}"
        params = {"api": self.api_key}
        params.update({k: v for k, v in kwargs.items() if v is not None})

        resp = await session.get(url, params=params)
        try:
            try:
                data = await resp.json(content_type=None)
            except Exception:
                data = await resp.text()

            if resp.status == 200:
                return data

            if resp.status == 400:
                raise BadRequestError()

            if resp.status == 429:
                raise RateLimitError()

            raise UnexpectedStatusError(
                f"Unexpected status {resp.status}: {data}"
            )
        finally:
            resp.release()

    async def make_request(
        self,
        endpoint: Any,
        *,
        retries: int = 3,
        retry_delay: int = 5,
        **kwargs: Any,
    ) -> Any:
        for attempt in range(retries + 1):
            try:
                return await self._make_request(
                    self.session, endpoint, **kwargs
                )

            except RateLimitError:
                if attempt >= retries:
                    raise
                await asyncio.sleep(retry_delay)

            except (
                ClientError,
                ClientConnectorError,
                InvalidURL,
                ServerTimeoutError,
                ContentTypeError,
            ) as exc:
                if attempt >= retries:
                    raise APIError(str(exc)) from exc
                await asyncio.sleep(retry_delay)


API = VoxylAPI()


SkinStyle = Literal[
    "face",
    "front",
    "frontfull",
    "head",
    "bust",
    "full",
    "skin",
    "processedskin",
]

DEFAULT_STEVE_SKIN_URL = (
    "https://textures.minecraft.net/texture/"
    "a4665d6a9c07b7b3ecf3b9f4b1c6bff0e43a9a3b65e5b4b94a3a4567d9a12345"
)


_skin_session = CachedSession(
    cache=skin_cache,
    timeout=ClientTimeout(total=5),
)


async def close_skin_session():
    await _skin_session.close()


async def fetch_skin_model(
    uuid: str,
    style: SkinStyle = "full",
) -> bytes:
    base_url = "https://visage.surgeplay.com"
    headers = {"User-Agent": "Voxyl Client"}
    url = f"{base_url}/{style}/512/{uuid}"

    try:
        res = await _skin_session.get(url, headers=headers)
        try:
            if res.status == 200:
                return await res.read()
            raise UnexpectedStatusError(
                f"Skin fetch failed with status {res.status}"
            )
        finally:
            res.release()

    except Exception:
        res = await _skin_session.get(
            DEFAULT_STEVE_SKIN_URL, headers=headers
        )
        try:
            return await res.read()
        finally:
            res.release()