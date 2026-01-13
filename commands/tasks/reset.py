import time

from discord.ext import commands, tasks

from logger import logger
from core.api.helpers import PlayerInfo
from database.handlers import HistoricalHandler


RESET_INTERVALS = {
    "daily": 60 * 60 * 24,
    "weekly": 60 * 60 * 24 * 7,
    "monthly": 60 * 60 * 24 * 30,
    "yearly": 60 * 60 * 24 * 365,
}

async def update_historical(period: str) -> None:
    now = int(time.time())
    interval = RESET_INTERVALS[period]

    handler = HistoricalHandler(None, period)
    players = handler.get_players()

    for uuid, last_reset in players:
        if now <= last_reset + interval:
            continue

        try:
            player_stats = await PlayerInfo.fetch(uuid)

            HistoricalHandler(uuid, period).upsert_stats(
                player_stats.wins,
                player_stats.weightedwins,
                player_stats.kills,
                player_stats.finals,
                player_stats.beds,
                player_stats.level,
                player_stats.exp
            )

        except Exception as error:
            logger.error(error)


async def update_daily():
    await update_historical("daily")

async def update_weekly():
    await update_historical("weekly")

async def update_monthly():
    await update_historical("monthly")

async def update_yearly():
    await update_historical("yearly")


class HistoricalReset(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.update_task.start()

    @tasks.loop(minutes=1)
    async def update_task(self):
        try:
            await update_daily()
            await update_weekly()
            await update_monthly()
            await update_yearly()

        except Exception as error:
            logger.error(error)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HistoricalReset(client))