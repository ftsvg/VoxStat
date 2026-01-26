from discord import Interaction, File

from mcfetch import Player

from core.api.helpers import PlayerInfo
from core import mojang_session
from content import ERRORS, DESCRIPTIONS
from database import HistoricalStats
from database.handlers import HistoricalHandler
from core.rendering.stats import render_historical
from .player import fetch_player
from logger import logger


PERIOD_SECONDS = {
    "daily": 86400,
    "weekly": 86400 * 7,
    "monthly": 86400 * 30,
    "yearly": 86400 * 365,
}


async def historical_interaction(
    interaction: Interaction,
    period: str,
    player: str | None 
) -> None:
    
    try:
        if not (uuid := await fetch_player(interaction, player)):
            return None

        player_stats = await PlayerInfo.fetch(uuid)
        historical_data = HistoricalHandler(uuid, period) 

        ign = Player(
            player=uuid, requests_obj=mojang_session
        ).name

        stats: HistoricalStats = historical_data.get_stats()
        if not stats:
            periods = ['daily', 'weekly', 'monthly', 'yearly']
        
            wins = player_stats.wins
            weighted =  player_stats.weightedwins
            kills = player_stats.kills
            finals = player_stats.finals
            beds = player_stats.beds
            level = player_stats.level
            xp = player_stats.exp

            for p in periods:
                HistoricalHandler(uuid, p).upsert_stats(
                    wins, weighted, kills, finals, beds, level, xp
                )

            return await interaction.edit_original_response(
                content=DESCRIPTIONS['historical_stats_tracked'].format(ign)
            )
        
        else:
            reset = stats.last_reset + PERIOD_SECONDS[period.lower()]
            
            await render_historical(
                player_stats, uuid, period, reset
            )

            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/historical.png")]
            )


    except Exception as error:
        logger.exception("Unhandled exception: %s", error)

        return await interaction.edit_original_response(
            content=ERRORS['application_error']
        )
