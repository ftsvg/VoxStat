from datetime import date, time, timezone
from discord.ext import commands, tasks
from discord import Embed, File
import time as time_mod
import asyncio
import json

from mcfetch import Player

from database.handlers import ChartsHandler, UserHandler, ChannelsHandler, GuildsHandler
from database import Charts, Users
from core import split_list, get_stars_gained, MAIN_COLOR, generate_xp_chart, mojang_session
from core.api.helpers import PlayerInfo

ONE_WEEK = 60 * 60 * 24 * 7


class XpCharts(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.xp_charts.start()

    async def run_xp_charts(self, *, force: bool = False):
        current_day = date.today()

        if not force and current_day.weekday() != 0:
            return

        charts_handler = ChartsHandler()
        charts: Charts | None = charts_handler.get_last_send()

        now_unix = int(time_mod.time())

        if not force and charts and charts.last_xp_chart:
            if now_unix - charts.last_xp_chart < ONE_WEEK:
                return

        users: list[Users] = UserHandler().get_all_users()
        if not users:
            return

        all_uuids = split_list([user.uuid for user in users])

        for uuids in all_uuids:
            for uuid in uuids:
                user_handler = UserHandler(uuid)
                user_data: Users = user_handler.get_user()

                if not user_data or not user_data.star or not user_data.xp:
                    continue

                stats = await PlayerInfo.fetch(uuid)
                if not stats:
                    continue

                stars_gained = get_stars_gained(
                    user_data.star, user_data.xp, stats.level, stats.exp
                )

                past_weeks = (
                    json.loads(user_data.past_star_weeks)
                    if isinstance(user_data.past_star_weeks, str)
                    else list(user_data.past_star_weeks)
                )

                past_weeks.insert(0, stars_gained)
                past_weeks = past_weeks[:5]

                highest_star = max(stars_gained, user_data.highest_star)

                user_handler.update_user(
                    stats.level,
                    stats.exp,
                    highest_star,
                    json.dumps(past_weeks),
                )

            await asyncio.sleep(60)

        channel_id = ChannelsHandler().get_channel("xp_charts")
        channel = await self.client.fetch_channel(channel_id)
        if not channel:
            return

        embed = Embed(
            title="XP Charts",
            description=(
                "XP Charts for all the guilds currently being tracked. "
                "You can add or remove guilds with **/admin addguild** and "
                "**/admin removeguild**"
            ),
            color=MAIN_COLOR,
        )

        await channel.send(embed=embed)

        for guild in GuildsHandler().get_all_guilds():
            guild_id = guild.guild_id
            users = UserHandler().get_guild_members(guild_id)

            x, y, colors = [], [], []

            for user in users:
                past_weeks = (
                    json.loads(user.past_star_weeks)
                    if isinstance(user.past_star_weeks, str)
                    else user.past_star_weeks
                )
                past_week = past_weeks[1] if past_weeks else 0

                ign = Player(player=user.uuid, requests_obj=mojang_session).name

                x.append(ign)
                y.append(past_week)
                colors.append("#1685F8" if past_week >= 2 else "#F32C55")

            await generate_xp_chart(
                x, y, colors,
                charts.last_xp_chart if charts else None,
                guild_id,
                True,
            )
            await channel.send(file=File("./assets/charts/xp_chart.png"))

        ChartsHandler().update_xp_last_send(now_unix)
        await asyncio.sleep(5)

    @tasks.loop(time=time(hour=6, minute=0, tzinfo=timezone.utc))
    async def xp_charts(self):
        await self.run_xp_charts()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(XpCharts(client))