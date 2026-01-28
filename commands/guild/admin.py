from discord.ext import commands
from discord import app_commands, Permissions, Interaction, TextChannel

from core import check_server
from core.api.helpers import GuildInfo
from logger import logger
from content import ERRORS
from database.handlers import GuildsHandler, ChannelsHandler


class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    
    admin = app_commands.Group(
        name="admin", 
        description="Admin related commands",
        default_permissions=Permissions(administrator=True)
    )    


    @admin.command(
        name=f"addguild", 
        description="Track a new guild"
    )
    @app_commands.describe(
        tag="The tag of the guild",
        logs_channel="The guild logs channel"
    )    
    async def addguild(
        self, 
        interaction: Interaction, 
        tag: str,
        logs_channel: TextChannel
    ):
        if not await check_server(interaction):
            return          

        try:    
            await interaction.response.defer()

            data = await GuildInfo.fetch(tag)
            if data is None:
                return await interaction.edit_original_response(
                    content=f"**{tag}** does not exist."
                )
            
            guild = GuildsHandler(data.id).get_guild()
            if guild:
                return await interaction.edit_original_response(
                    content="This guild is already being tracked."
                )

            ChannelsHandler().set_guild_logs_channel(
                data.id, logs_channel.id
            )
            GuildsHandler(data.id).set_guild(data.xp)

            return await interaction.edit_original_response(
                content=(
                    f"**{data.name}** `[{tag.upper()}]` `({data.id})` will now be tracked. "
                    f"Guild logs will be sent to {logs_channel.mention}"
                )
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


    @admin.command(
        name=f"removeguild", 
        description="Remove a tracked guild"
    )
    @app_commands.describe(
        tag="The tag of the guild",
    )    
    async def removeguild(
        self, 
        interaction: Interaction, 
        tag: str,
    ):
        if not await check_server(interaction):
            return          

        try:    
            await interaction.response.defer()

            data = await GuildInfo.fetch(tag)
            if data is None:
                return await interaction.edit_original_response(
                    content=f"**{tag}** does not exist."
                )
            
            guild = GuildsHandler(data.id).get_guild()
            if not guild:
                return await interaction.edit_original_response(
                    content="This guild is not currently being tracked."
                )

            ChannelsHandler().delete_guild_logs_channel(
                data.id
            )
            GuildsHandler(data.id).remove_guild()

            return await interaction.edit_original_response(
                content=f"**{data.name}** `[{tag.upper()}]` `({data.id})` has been removed."
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


    @admin.command(
        name="channel", 
        description="sets the discord output channel for different bot functions"
    )
    @app_commands.describe(
        channel_type="The channel type you want to set", 
        channel="The output channel"
    )
    @app_commands.choices(
        channel_type=[
            app_commands.Choice(name="xp_charts", value="xp_charts"),
            app_commands.Choice(name="gxp_charts", value="gxp_charts"),
            app_commands.Choice(name="applications", value="applications"),
        ]
    )
    async def channel(
        self, 
        interaction: Interaction, 
        channel_type: str, 
        channel: TextChannel
    ):
        if not await check_server(interaction):
            return
        
        try:
            await interaction.response.defer()

            ChannelsHandler().set_channel(channel.id, channel_type)
            return await interaction.edit_original_response(
                content=f"**{channel_type}** has been set to {channel.mention}"
            )

        except Exception as error:
            logger.exception("Unhandled exception: %s", error)
            await interaction.edit_original_response(
                content=ERRORS['application_error']
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin(client)) 