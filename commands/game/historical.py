from discord.ext import commands
from discord import app_commands, Interaction

from core import historical_interaction


class Historical(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    historical = app_commands.Group(
        name="historical", 
        description="Historical related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )


    @historical.command(
        name="daily", 
        description="View the daily stats of a player"
    )
    @app_commands.describe(
        player="The player you want to view"
    )
    async def daily(self, interaction: Interaction, player: str = None):
        await interaction.response.defer()
        await historical_interaction(interaction, "daily", player)


    @historical.command(
        name="weekly", 
        description="View the weekly stats of a player"
    )
    @app_commands.describe(
        player="The player you want to view"
    )
    async def weekly(self, interaction: Interaction, player: str = None):
        await interaction.response.defer()
        await historical_interaction(interaction, "weekly", player)


    @historical.command(
        name="monthly", 
        description="View the monthly stats of a player"
    )
    @app_commands.describe(
        player="The player you want to view"
    )
    async def monthly(self, interaction: Interaction, player: str = None):
        await interaction.response.defer()
        await historical_interaction(interaction, "monthly", player)


    @historical.command(
        name="yearly", 
        description="View the yearly stats of a player"
    )
    @app_commands.describe(player="The player you want to view")
    async def yearly(self, interaction: Interaction, player: str = None):
        await interaction.response.defer()
        await historical_interaction(interaction, "yearly", player)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Historical(client)) 