from discord import Interaction, app_commands
from discord.ext import commands

from views import SuggestionModal, BugReportModal
from config import Settings


class Support(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client


    @app_commands.command(
        name="support",
        description="Get in contact with support, suggest a feature or report a bug"
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        type="Select a what you want to do"
    )
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Support", value="support"),
            app_commands.Choice(name="Suggestion", value="suggestion"),
            app_commands.Choice(name="Bug report", value="bug"),
        ]
    )
    async def support(
        self,
        interaction: Interaction,
        type: str
    ):
        if type == "support":
            await interaction.response.send_message(
                content=(
                    f"For support, please join our [**support server**](<{Settings.SUPPORT_SERVER}>)"
                ),
                ephemeral=True
            )
        
        if type == "suggestion":
            await interaction.response.send_modal(
                SuggestionModal(interaction.user)
            )

        if type == "bug":
            await interaction.response.send_modal(
                BugReportModal(interaction.user)
            )
        

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Support(client))