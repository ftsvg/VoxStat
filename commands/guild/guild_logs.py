import asyncio
import json
from discord import TextChannel, Embed
from discord.ext import commands, tasks

from logger import logger
from database.handlers import GuildsHandler, UserHandler, ChannelsHandler
from database import Guilds
from core.api.helpers import GuildInfo, PlayerInfo


class GuildLogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.loop.create_task(self.start_loop())

    async def start_loop(self):
        await self.client.wait_until_ready()
        if not self.guild_logs.is_running():
            self.guild_logs.start()

    @tasks.loop(minutes=15)
    async def guild_logs(self):
        try:
            guilds = GuildsHandler().get_all_guilds()

            guild_infos = await asyncio.gather(
                *(GuildInfo.fetch(guild.guild_id) for guild in guilds),
                return_exceptions=True
            )

            new_all_members = [
                info.members if not isinstance(info, Exception) and info else []
                for info in guild_infos
            ]

            old_all_members = [
                UserHandler().get_old_guild_members(guild.guild_id) or []
                for guild in guilds
            ]

            for i, guild in enumerate(guilds):
                new_members = [u.replace("-", "") for u in new_all_members[i]]
                old_members = [u.replace("-", "") for u in old_all_members[i]]

                joined_uuids = list(set(new_members) - set(old_members))
                left_uuids = list(set(old_members) - set(new_members))

                joined_infos = await asyncio.gather(
                    *(PlayerInfo.fetch(uuid) for uuid in joined_uuids),
                    return_exceptions=True
                )

                left_infos = await asyncio.gather(
                    *(PlayerInfo.fetch(uuid) for uuid in left_uuids),
                    return_exceptions=True
                )

                channel_id = ChannelsHandler().get_guild_logs_channel(guild.guild_id)
                channel: TextChannel = await self.client.fetch_channel(channel_id)

                for idx, info in enumerate(joined_infos):
                    if isinstance(info, Exception):
                        continue
                    ign = info.last_login_name
                    if ign and channel:
                        await self.joined(
                            ign,
                            joined_uuids[idx],
                            guild,
                            channel,
                            info
                        )

                for idx, info in enumerate(left_infos):
                    if isinstance(info, Exception):
                        continue
                    ign = info.last_login_name
                    if ign and channel:
                        await self.left(
                            ign,
                            left_uuids[idx],
                            guild,
                            channel
                        )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)

    async def joined(
        self,
        ign: str,
        uuid: str,
        guild: Guilds,
        channel: TextChannel,
        info: PlayerInfo
    ):
        embed = Embed(color=0x90EE90)
        embed.set_author(
            name=f"{ign} joined the guild",
            icon_url=f"https://cravatar.eu/helmavatar/{uuid}/64"
        )
        await channel.send(embed=embed)

        user_handler = UserHandler(uuid)
        user = user_handler.get_user()

        if user:
            user_handler.set_guild(guild.guild_id)
        else:
            user_handler.insert_new_user(
                discord_id=None,
                guild_id=guild.guild_id,
                star=info.level,
                xp=info.exp,
                highest_star=0.0,
                past_star_weeks=json.dumps([0.0, 0.0, 0.0, 0.0, 0.0]),
                tracklist=False
            )

    async def left(
        self,
        ign: str,
        uuid: str,
        guild: Guilds,
        channel: TextChannel
    ):
        embed = Embed(color=0xFF7276)
        embed.set_author(
            name=f"{ign} left (or was kicked) from the guild",
            icon_url=f"https://cravatar.eu/helmavatar/{uuid}/64"
        )
        await channel.send(embed=embed)

        user_handler = UserHandler(uuid)
        user = user_handler.get_user()

        if user and user.guild_id == guild.guild_id:
            user_handler.set_guild(None)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GuildLogs(client))
