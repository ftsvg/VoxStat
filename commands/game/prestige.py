from discord.ext import commands
from discord import app_commands, Interaction, File

from core import SESSION_CHOICES, fetch_player
from content import ERRORS
from core.api.helpers import PlayerInfo
from logger import logger
from content import ERRORS
from database.handlers import SessionHandler

from core.rendering.stats import render_projected


class Prestige(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(
        name="prestige", 
        description="Get your projected stats based on a session"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        level="The level to get projected stats for",
        player="The player you want to view",
        session="The session you want to view (default 1)"
    )
    @app_commands.choices(session=SESSION_CHOICES)
    async def prestige(
        self, 
        interaction: Interaction,
        level: int,
        player: str = None,
        session: int = 1
    ):
        await interaction.response.defer()
        try:
            if not (uuid := await fetch_player(interaction, player)):
                return None
            
            handler = SessionHandler(uuid, session)
            session_stats = handler.get_session()

            if not session_stats:
                await handler.create_session()
                return await interaction.edit_original_response(
                    content=ERRORS['no_session_found'].format(session)
                )

            stats = await PlayerInfo.fetch(uuid)
            plevel = stats.level

            if plevel > 9999:
                return await interaction.edit_original_response(
                    content=f"The prestige level cannot be higher than **9999**"
                )
                

            if level <= plevel:
                return await interaction.edit_original_response(
                    content=f"The prestige level must be higher than the player's current level."
                )

            render_error = await render_projected(
                uuid, stats, session_stats, level
            )
            if render_error:
                await interaction.edit_original_response(content=render_error)

            else:
                await interaction.edit_original_response(
                    attachments=[File(f"./assets/stats/projected.png")]
                )
                    
        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Prestige(client))