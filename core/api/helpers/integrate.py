import asyncio

from core.api import API, VoxylApiEndpoint, APIError, RateLimitError


class IntegrationInfo:
    def __init__(
        self,
        discord_from_player: dict | int,
        player_from_discord: dict | int,
    ):
        self.discord_from_player = discord_from_player
        self.player_from_discord = player_from_discord

        self.discord_id = (
            discord_from_player.get("id")
            if isinstance(discord_from_player, dict)
            else discord_from_player
        )

        self.player_uuid = (
            player_from_discord.get("uuid")
            if isinstance(player_from_discord, dict)
            else player_from_discord
        )

    @classmethod
    async def fetch(
        cls,
        *,
        uuid: str | None = None,
        discord_id: str | None = None,
    ) -> "IntegrationInfo":
        async def safe(
            endpoint: VoxylApiEndpoint,
            **params: str,
        ) -> dict | int:
            try:
                return await API.make_request(endpoint, **params)
            except RateLimitError:
                return 429
            except APIError:
                return 500

        tasks = []

        if uuid is not None:
            tasks.append(
                safe(
                    VoxylApiEndpoint.DISCORD_FROM_PLAYER,
                    uuid=uuid,
                )
            )
        else:
            tasks.append(asyncio.sleep(0, result=None))

        if discord_id is not None:
            tasks.append(
                safe(
                    VoxylApiEndpoint.PLAYER_FROM_DISCORD,
                    discord_id=discord_id,
                )
            )
        else:
            tasks.append(asyncio.sleep(0, result=None))

        discord_from_player, player_from_discord = await asyncio.gather(
            *tasks
        )

        return cls(
            discord_from_player,
            player_from_discord,
        )