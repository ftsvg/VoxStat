import json

from discord.ext import commands
from discord import app_commands, Interaction, File

from logger import logger
from content import ERRORS
from core import MAIN_COLOR, check_server, generate_xp_chart
from core.api.helpers import GuildInfo, PlayerInfo
from database.handlers import UserHandler, GuildsHandler, ChartsHandler
from database import Charts


class Preview(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    preview = app_commands.Group(
        name="preview", 
        description="Preview related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )


    @preview.command(
        name="xp",
        description="Shows xp progress for given guild"
    )
    @app_commands.describe(
        tag="The guild you want to view"
    )
    async def xp_chart(
        self,
        interaction: Interaction,
        tag: str = "SHINE"
    ):
        try:
            if not await check_server(interaction):
                return

            await interaction.response.defer()

            data = await GuildInfo.fetch(tag)
            if not data:
                return await interaction.edit_original_response(
                    content=f"**{tag.upper()}** does not exist."
                )

            guild = GuildsHandler(data.id).get_guild()
            if not guild:
                return await interaction.edit_original_response(
                    content=f"**{tag.upper()}** is not currently being tracked."
                )

            charts: Charts = ChartsHandler().get_last_send()
            last_updated = charts.last_xp_chart if charts else None

            users = UserHandler().get_guild_members(guild.guild_id)
            if not users:
                return await interaction.edit_original_response(
                    content="No users found for this guild."
                )

            x, y, colors = [], [], []

            for user in users:
                past_weeks = (
                    json.loads(user.past_star_weeks)
                    if isinstance(user.past_star_weeks, str)
                    else user.past_star_weeks
                )

                past_week = past_weeks[2] if past_weeks else 0

                info = await PlayerInfo.fetch(user.uuid)
                if not info or not info.last_login_name:
                    continue

                x.append(info.last_login_name)
                y.append(past_week)
                colors.append("#1685F8" if past_week >= 2 else "#F32C55")

            await generate_xp_chart(
                x,
                y,
                colors,
                last_updated,
                guild.guild_id,
                True,
            )

            await interaction.edit_original_response(
                attachments=[File("./assets/charts/xp_chart.png")]
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS["application_error"]
            )
 


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Preview(client))