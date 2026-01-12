import asyncio
from typing import Any

from core.api import API, VoxylApiEndpoint, APIError, RateLimitError


class PlayerInfo:
    def __init__(
        self,
        uuid: str,
        player_info: dict | int,
        overall_stats: dict | int,
        game_stats: dict | int,
        guild_info: dict | int,
    ):
        self.uuid = uuid

        self.player_info = player_info
        self.overall_stats = overall_stats
        self.game_stats = game_stats
        self.guild_info = guild_info

        self.last_login_name = (
            player_info.get("lastLoginName")
            if isinstance(player_info, dict)
            else player_info
        )

        self.last_login_time = (
            player_info.get("lastLoginTime")
            if isinstance(player_info, dict)
            else player_info
        )

        self.role = (
            player_info.get("role")
            if isinstance(player_info, dict)
            else player_info
        )

        self.level = (
            overall_stats.get("level")
            if isinstance(overall_stats, dict)
            else overall_stats
        )

        self.exp = (
            overall_stats.get("exp")
            if isinstance(overall_stats, dict)
            else overall_stats
        )

        self.weightedwins = (
            overall_stats.get("weightedwins")
            if isinstance(overall_stats, dict)
            else overall_stats
        )

        stats = (
            game_stats.get("stats")
            if isinstance(game_stats, dict)
            else None
        )

        self.wins = (
            sum(s.get("wins", 0) for s in stats.values())
            if stats
            else game_stats
        )

        self.kills = (
            sum(s.get("kills", 0) for s in stats.values())
            if stats
            else game_stats
        )

        self.finals = (
            sum(s.get("finals", 0) for s in stats.values())
            if stats
            else game_stats
        )

        self.beds = (
            sum(s.get("beds", 0) for s in stats.values())
            if stats
            else game_stats
        )

        self.guild_role = (
            guild_info.get("guildRole")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.guild_join_time = (
            guild_info.get("joinTime")
            if isinstance(guild_info, dict)
            else guild_info
        )

        self.guild_id = (
            guild_info.get("guildId")
            if isinstance(guild_info, dict)
            else guild_info
        )

    @classmethod
    async def fetch(cls, uuid: str) -> "PlayerInfo":
        async def safe(endpoint: VoxylApiEndpoint) -> dict | int:
            try:
                return await API.make_request(endpoint, uuid=uuid)
            except RateLimitError:
                return 429
            except APIError:
                return 500

        player_info, overall_stats, game_stats, guild_info = await asyncio.gather(
            safe(VoxylApiEndpoint.PLAYER_INFO),
            safe(VoxylApiEndpoint.PLAYER_OVERALL),
            safe(VoxylApiEndpoint.PLAYER_STATS),
            safe(VoxylApiEndpoint.PLAYER_GUILD),
        )

        return cls(
            uuid,
            player_info,
            overall_stats,
            game_stats,
            guild_info,
        )