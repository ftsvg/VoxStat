from discord.ext import commands
from discord import app_commands, Interaction, File

from logger import logger
from content import ERRORS
from core import check_server, fetch_player
from core.rendering.stats import render_check
from database.handlers import UserHandler


class Check(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(
        name="check", 
        description="View xp progress and weekly stats for any player"
    )
    @app_commands.describe(
        player="The player you want to view",
    )
    async def check(
        self, 
        interaction: Interaction,
        player: str = None
    ):
        try:
            if not await check_server(interaction):
                return            
            
            await interaction.response.defer()
            if not (uuid := await fetch_player(interaction, player)):
                return None

            user_data = UserHandler(uuid).get_user()
            if not user_data: 
                return await interaction.edit_original_response(
                    content="This user is currently not tracked."
                )

            await render_check(uuid, user_data)

            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/check.png")],
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 



async def setup(client: commands.Bot) -> None:
    await client.add_cog(Check(client))