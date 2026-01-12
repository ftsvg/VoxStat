import asyncio
from typing import Any

from core.api import API, VoxylApiEndpoint, APIError, RateLimitError


class GuildInfo:
    def __init__(
        self,
        tag_or_id: str,
        guild_info: dict | int,
        guild_members: dict | int,
    ):
        self.tag_or_id = tag_or_id

        self.guild_info = guild_info
        self.guild_members = guild_members

        self.id = (
            guild_info.get("id")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.name = (
            guild_info.get("name")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.description = (
            guild_info.get("desc")
            if isinstance(guild_info, dict)
            else guild_info
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
            guild_info.get("ownerUUID")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.creation_time = (
            guild_info.get("time")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.members = (
            guild_members.get("members")
            if isinstance(guild_members, dict)
            else guild_members
        )

    @classmethod
    async def fetch(cls, tag_or_id: str) -> "GuildInfo":
        async def safe(
            endpoint: VoxylApiEndpoint,
            **params: Any,
        ) -> dict | int:
            try:
                return await API.make_request(endpoint, **params)
            except RateLimitError:
                return 429
            except APIError:
                return 500

        guild_info, guild_members = await asyncio.gather(
            safe(
                VoxylApiEndpoint.GUILD_INFO,
                tag_or_id=tag_or_id,
            ),
            safe(
                VoxylApiEndpoint.GUILD_MEMBERS,
                tag_or_id=tag_or_id,
            ),
        )

        return cls(
            tag_or_id,
            guild_info,
            guild_members,
        )

    @staticmethod
    async def fetch_top_guilds(
        num: int = 10,
    ) -> dict | int:
        try:
            return await API.make_request(
                VoxylApiEndpoint.GUILD_TOP,
                num=num,
            )
        except RateLimitError:
            return 429
        except APIError:
            return 500