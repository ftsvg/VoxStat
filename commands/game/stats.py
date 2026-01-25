from discord.ext import commands
from discord import app_commands, Interaction, File

from logger import logger
from content import ERRORS
from core import fetch_player, MODES
from core.rendering.stats import render_stats
from core.api.helpers import PlayerInfo
from views import StatsView


class Stats(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(
        name="stats", 
        description="Shows players stats"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.choices(mode=MODES)
    @app_commands.describe(
        player="The player you want to view",
        mode="The mode you want to view"
    )
    async def stats(
        self, 
        interaction: Interaction, 
        player: str = None, 
        mode: str = "Overall"
    ):
        await interaction.response.defer()
        try:
            if not (uuid := await fetch_player(interaction, player)):
                return None
            
            stats = await PlayerInfo.fetch(uuid)
            await render_stats(stats, mode, uuid, "combined")

            view = StatsView(
                interaction=interaction,
                uuid=uuid,
                org_user=interaction.user.id,
                mode=mode,
                player=stats
            )

            await interaction.edit_original_response(
                content=f"Last login time: <t:{stats.last_login_time}:R>",
                attachments=[File(f"./assets/stats/stats.png")],
                view=view
            )

        except Exception as error:
            logger.warning(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Stats(client))