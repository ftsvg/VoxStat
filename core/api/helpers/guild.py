import asyncio
from typing import Any

from core.api import API, VoxylApiEndpoint, APIError, RateLimitError


class GuildInfo:
    def __init__(
        self,
        tag_or_id: str,
        guild_info: dict | int | None,
        guild_members: dict | int | None,
    ):
        self.tag_or_id = str(tag_or_id)

        self.id = (
            str(guild_info.get("id"))
            if isinstance(guild_info, dict)
            else str(guild_info)
        )

        self.name = (
            str(guild_info.get("name"))
            if isinstance(guild_info, dict)
            else str(guild_info)
        )

        self.description = (
            str(guild_info.get("desc"))
            if isinstance(guild_info, dict)
            else str(guild_info)
        )

        self.xp = (
            guild_info.get("xp")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.member_count = (
            guild_info.get("num")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.owner_uuid = (
            str(guild_info.get("ownerUUID"))
            if isinstance(guild_info, dict)
            else str(guild_info)
        )

        self.creation_time = (
            guild_info.get("time")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.members = (
            [m["uuid"] for m in guild_members.get("members", [])]
            if isinstance(guild_members, dict)
            else []
        )

    @classmethod
    async def fetch(cls, tag_or_id: str | int) -> "GuildInfo | None":
        def normalize(value: str | int) -> str:
            value = str(value)
            return f"-{value}" if value.isdigit() else value

        async def safe(
            endpoint: VoxylApiEndpoint,
            **params: Any,
        ) -> dict | int | None:
            try:
                return await API.make_request(endpoint, **params)
            except (RateLimitError, APIError):
                return None

        identifier = normalize(tag_or_id)

        guild_info, guild_members = await asyncio.gather(
            safe(
                VoxylApiEndpoint.GUILD_INFO,
                tag_or_id=identifier,
            ),
            safe(
                VoxylApiEndpoint.GUILD_MEMBERS,
                tag_or_id=identifier,
            ),
        )

        if guild_info is None:
            return None

        return cls(
            identifier,
            guild_info,
            guild_members,
        )

    @staticmethod
    async def fetch_top_guilds(num: int = 10) -> dict | int:
        try:
            return await API.make_request(
                VoxylApiEndpoint.GUILD_TOP,
                num=num,
            )
        except RateLimitError:
            return 429
        except APIError:
            return 500