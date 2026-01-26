import json

from mcfetch import Player
from discord import Interaction, Embed

from content import ERRORS
from core.api.helpers import IntegrationInfo, PlayerInfo
from database.handlers import UserHandler
from database import Users
from logger import logger
from core import check_if_valid_ign, mojang_session, MAIN_COLOR


async def link_interaction(
    interaction: Interaction,
    player: str | None,
) -> None:
    try:
        uuid = await check_if_valid_ign(interaction, player)
        if not uuid:
            return

        userhandler = UserHandler(uuid)
        user = userhandler.get_user()

        if user and user.discord_id:
            ign = Player(player=uuid, requests_obj=mojang_session).name
            await interaction.edit_original_response(
                content=ERRORS["already_linked"].format(ign)
            )
            return

        integration = await IntegrationInfo.fetch(
            uuid=uuid,
            discord_id=interaction.user.id,
        )

        if not integration or any(
            x in (None, 429, 500)
            for x in (integration.discord_id, integration.player_uuid)
        ):
            embed = Embed(
                title="Player Not Integrated To Voxyl Network",
                color=MAIN_COLOR,
                description=(
                    "To successfully link your account, please ensure that "
                    "you're using the correct IGN and Discord account that "
                    "is integrated to the Voxyl Network.\n\n"
                    "**Follow the steps below to integrate:**\n"
                    "> `1.` Join the official Bedwars Practice Discord "
                    "[here](https://discord.gg/7Mt7T8hqr4)\n"
                    "> `2.` Go to the integration channel\n"
                    "> `3.` Join **sync.voxyl.net** in Minecraft\n"
                    "> `4.` Copy the integration code shown in-game\n"
                    "> `5.` Run **;integrate <ign> <code>** in Discord\n"
                    "> `6.` After integration, run **/link <ign>** again\n"
                ),
            )
            await interaction.edit_original_response(embed=embed)
            return

        if interaction.user.id != integration.discord_id:
            ign = Player(
                player=str(integration.player_uuid).replace("-", ""),
                requests_obj=mojang_session
            ).name
            await interaction.edit_original_response(
                content=ERRORS["integrated_to_other_account"].format(ign, ign)
            )
            return

        ign = Player(player=uuid, requests_obj=mojang_session).name

        if user:
            userhandler.verify_user(interaction.user.id)
        else:
            player_stats = await PlayerInfo.fetch(uuid)
            userhandler.insert_new_user(
                discord_id=interaction.user.id,
                guild_id=player_stats.guild_id,
                star=player_stats.level,
                xp=player_stats.exp,
                highest_star=0.00,
                past_star_weeks=json.dumps([]),
                tracklist=False
            )

        await interaction.edit_original_response(
            content=f"You have successfully linked as **{ign}**."
        )

    except Exception as error:
        logger.exception("Unhandled exception: %s", error)
        await interaction.edit_original_response(
            content=ERRORS["application_error"]
        )


async def unlink_interaction(interaction: Interaction) -> None:
    try:
        handler = UserHandler(None)

        user = handler.get_user_by_discord_id(interaction.user.id)
        if not user:
            await interaction.edit_original_response(
                content=ERRORS["account_not_linked"]
            )
            return
        
        handler.unverify_user(interaction.user.id)

        await interaction.edit_original_response(
            content="You have been successfully unlinked."
        )

    except Exception as error:
        logger.exception("Unhandled exception: %s", error)
        await interaction.edit_original_response(
            content=ERRORS['application_error']
        )