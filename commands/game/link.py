from discord.ext import commands
from discord import app_commands, Interaction

from core import link_interaction, unlink_interaction
from content import COMMANDS


class Linking(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client


    @app_commands.command(
            name=COMMANDS['link']['name'], 
            description=COMMANDS['link']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.describe(
        player=COMMANDS['link']['player']
    )
    async def link(
        self, interaction: Interaction, player: str, 
    ):
        await interaction.response.defer()
        await link_interaction(interaction, player)


    @app_commands.command(
            name=COMMANDS['unlink']['name'], 
            description=COMMANDS['unlink']['description']
    )
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def unlink(
        self, interaction: Interaction
    ):
        await interaction.response.defer()
        await unlink_interaction(interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Linking(client))