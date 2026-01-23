from discord.ext import commands
from discord import app_commands, Interaction, File
from mcfetch import Player

from logger import logger
from core import PAGES, get_leaderboard_page, mojang_session
from core.api.helpers import LeaderboardInfo
from core.rendering.stats import render_leaderboard


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    leaderboard = app_commands.Group(
        name="leaderboard", 
        description="Leaderboard related commands",
        allowed_contexts=app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
        allowed_installs=app_commands.AppInstallationType(guild=True, user=True)
    )


    @leaderboard.command(
        name="level", 
        description="Shows top 100 level leaderboard"
    )
    @app_commands.describe(
        page="The page you want to view",
        player="The username of the player"
    )
    @app_commands.choices(page=PAGES)
    async def level(
        self, 
        interaction: Interaction, 
        page: int = 1, 
        player: str = None
    ):
        await interaction.response.defer()

        try:
            data = await LeaderboardInfo.fetch_leaderboard(
                _type='level', 
                num=100
            )

            if player:
                p_page, pos = get_leaderboard_page(data, player)

                if p_page is None and pos is None:
                    uuid = Player(player=player, requests_obj=mojang_session).uuid

                    if not uuid:
                        return await interaction.edit_original_response(
                            content=f"**{player}** does not exist! Please provide a valid username."
                        ) 
                    else:
                        return await interaction.edit_original_response(
                            content=f"**{player}** was not found on the level leaderboard."
                        )
                    
                page = p_page 
            else:
                pos = None
            

            await render_leaderboard(data, page, pos, 'Level')
            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/leaderboard_level.png")],
            )    

        except Exception as error:
            logger.warning(error)


    @leaderboard.command(
        name="weightedwins", 
        description="Shows top 100 weighted wins leaderboard"
    )
    @app_commands.describe(
        page="The page you want to view",
        player="The username of the player"
    )
    @app_commands.choices(page=PAGES)
    async def weightedwins(
        self, 
        interaction: Interaction, 
        page: int = 1, 
        player: str = None
    ):
        await interaction.response.defer()

        try:
            data = await LeaderboardInfo.fetch_leaderboard(
                _type='weightedwins', 
                num=100
            )

            if player:
                p_page, pos = get_leaderboard_page(data, player)

                if p_page is None and pos is None:
                    uuid = Player(player=player, requests_obj=mojang_session).uuid

                    if not uuid:
                        return await interaction.edit_original_response(
                            content=f"**{player}** does not exist! Please provide a valid username."
                        ) 
                    else:
                        return await interaction.edit_original_response(
                            content=f"**{player}** was not found on the leaderboard."
                        )
                    
                page = p_page 
            else:
                pos = None
            

            await render_leaderboard(data, page, pos, 'weightedwins')
            await interaction.edit_original_response(
                attachments=[File(f"./assets/stats/leaderboard_weightedwins.png")],
            )    

        except Exception as error:
            logger.warning(error)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Leaderboard(client))