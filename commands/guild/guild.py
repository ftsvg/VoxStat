from discord.ext import commands
from discord import app_commands, Interaction, Embed

from logger import logger
from content import ERRORS
from core import send_webhook_message, MAIN_COLOR, check_server
from core.api.helpers import GuildInfo


class Guild(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    guild = app_commands.Group(
        name="guild", 
        description="Guild related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )


    @guild.command(
        name="online", 
        description="Shows all online guild members"
    )
    @app_commands.describe(tag="The guild you want to view")
    async def online(
        self, 
        interaction: Interaction,
        tag: str = 'SHINE'
    ):
        try:
            if not await check_server(interaction):
                return
            
            await interaction.response.defer()

            data = await GuildInfo.fetch(tag)
            if data is None:
                return await interaction.edit_original_response(
                    content=f"**{tag}** does not exist."
                )

            guild_tag = tag.upper()

            response = await send_webhook_message(
                payload_type="guild_online",
                payload_content=f"/guild list {tag}",
                expect_response=True
            )

            if response is None:
                return await interaction.edit_original_response(
                    content=f"Failed to fetch guild members for {guild_tag}."
                )

            members = response.get("payload", {}).get("members", [])
            if not members:
                online = "No members online."
            else:
                online = ", ".join(members)

            await interaction.edit_original_response(
                embed=Embed(
                    title=f"{guild_tag} Online Members ({len(members)})", color=MAIN_COLOR,
                    description=f"```{online}```"
                )
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Guild(client))