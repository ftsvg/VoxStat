from discord.ext import commands
from discord import app_commands, Interaction, File

from logger import logger
from core import fetch_player
from core.api.helpers import PlayerInfo
from core.rendering.stats import render_compare


class Compare(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @app_commands.command(
        name="compare", 
        description="Compare player's stats to another player's stats"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        player_1="The primary player", 
        player_2="The secondary player"
    )
    async def compare(
        self, 
        interaction: Interaction, 
        player_1: str, 
        player_2: str = None
    ):
        await interaction.response.defer()
        try:
            player_1_uuid = await fetch_player(interaction, player_1)
            player_2_uuid = await fetch_player(interaction, player_2)

            if not player_1_uuid or not player_2_uuid:
                return None
            
            await render_compare(player_1_uuid, player_2_uuid)
            
            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/compare.png")]
            ) 
            
        except Exception as error:
            logger.warning(error)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Compare(client)) 