from discord.ext import commands
from discord import app_commands, Interaction, File

from content import ERRORS, DESCRIPTIONS
from core.rendering.stats import render_session
from core import SESSION_CHOICES
from logger import logger
from database.handlers import SessionHandler
from core import (
    check_if_linked_discord,
    fetch_player,
)


class Session(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    session = app_commands.Group(
        name="session",
        description="View and manage active sessions",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )


    @session.command(
        name="start", 
        description="Starts a new session")
    @app_commands.describe(
        session="The session you want to start"
    )
    @app_commands.choices(session=SESSION_CHOICES)
    async def start_session(self, interaction: Interaction, session: int):
        await interaction.response.defer()
        try:
            if not (uuid := await check_if_linked_discord(
                interaction, ERRORS['session_account_linked'])
            ):
                return None

            handler = SessionHandler(uuid, session)

            if handler.get_session():
                return await interaction.edit_original_response(
                    content=ERRORS['session_already_active'].format(session)
                )

            await handler.create_session()
            await interaction.edit_original_response(
                content=DESCRIPTIONS['session_started'].format(session)
            )

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


    @session.command(
        name="end", 
        description="Ends a session"
    )
    @app_commands.describe(
        session="The session you want to end"
    )
    @app_commands.choices(session=SESSION_CHOICES)
    async def end_session(self, interaction: Interaction, session: int):
        await interaction.response.defer()

        try:
            if not (uuid := await check_if_linked_discord(
                interaction, ERRORS['session_account_linked'])
            ):
                return None

            handler = SessionHandler(uuid, session)

            if not handler.get_session():
                return await interaction.edit_original_response(
                    content=ERRORS['session_not_active'].format(session)
                )

            handler.end_session()
            await interaction.edit_original_response(
                content=DESCRIPTIONS['session_deleted'].format(session)
            )

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


    @session.command(
        name="reset", 
        description="Resets a session"
    )
    @app_commands.describe(
        session="The session you want to reset"
    )
    @app_commands.choices(session=SESSION_CHOICES)
    async def reset_session(self, interaction: Interaction, session: int):
        await interaction.response.defer()
        try:
            if not (uuid := await check_if_linked_discord(
                interaction, ERRORS['session_account_linked'])
            ):
                return None

            handler = SessionHandler(uuid, session)

            if not handler.get_session():
                return await interaction.edit_original_response(
                    content=ERRORS['session_not_active'].format(session)
                )

            await handler.reset_session()
            await interaction.edit_original_response(
                content=DESCRIPTIONS['session_reset'].format(session)
            )

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


    @session.command(
        name="active", 
        description="View active sessions"
    )
    async def active_sessions(self, interaction: Interaction):
        await interaction.response.defer()
        try:
            if not (uuid := await check_if_linked_discord(
                interaction, ERRORS['session_account_linked'])
            ):
                return None

            sessions = SessionHandler(uuid, 1).get_active_sessions()

            if not sessions:
                return await interaction.edit_original_response(
                    content=ERRORS['no_active_sessions']
                )

            session_list = ", ".join(str(s) for s in sorted(sessions))
            await interaction.edit_original_response(
                content=DESCRIPTIONS['active_sessions'].format(session_list)
            )
    
        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


    @session.command(
        name="view", 
        description="View a player's session"
    )
    @app_commands.describe(
        player="The player you want to view",
        session="The session you want to view"
    )
    @app_commands.choices(session=SESSION_CHOICES)
    async def view_session(
        self,
        interaction: Interaction,
        player: str | None = None,
        session: int = 1,
    ):
        await interaction.response.defer()

        try:
            if not (uuid := await fetch_player(interaction, player)):
                return None

            handler = SessionHandler(uuid, session)

            if not handler.get_session():
                await handler.create_session()
                await interaction.edit_original_response(
                    content=ERRORS['no_session_found'].format(session)
                )
                return

            await render_session(uuid, session)
            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/session.png")]
            )

        except Exception as error:
            logger.error(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Session(client))