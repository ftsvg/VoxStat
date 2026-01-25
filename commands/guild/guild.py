from discord.ext import commands
from discord import app_commands, Interaction, Embed

from logger import logger
from content import ERRORS
from core import send_webhook_message, MAIN_COLOR


class Guild(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    guild = app_commands.Group(
        name="guild", 
        description="Guild related commands",
    )


    @guild.command(
        name="online", 
        description="Shows all online guild members"
    )
    async def online(
        self, 
        interaction: Interaction, 
    ):
        await interaction.response.defer()

        try:
            response = await send_webhook_message(
                payload_type="guild_online",
                payload_content="/guild online",
                expect_response=True
            )

            if response is None:
                return await interaction.edit_original_response(
                    content="Failed to fetch guild members."
                )

            members = response.get("payload", {}).get("members", [])

            await interaction.edit_original_response(
                embed=Embed(
                    title="Online Members", color=MAIN_COLOR,
                    description=f"```{", ".join(members)}```"
                )
            )

        except Exception as error:
            logger.warning(error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            ) 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Guild(client))