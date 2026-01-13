from mcfetch import Player
from discord import Interaction, Embed

from content import ERRORS
from core.api.helpers import IntegrationInfo
from database.handlers import LinkHandler
from database import LinkedPlayer
from logger import logger
from core import check_if_valid_ign, mojang_session, MAIN_COLOR


async def link_interaction(
    interaction: Interaction,
    player: str | None,
) -> None:
    try:
        linked = LinkHandler(interaction.user.id).get_linked_player()
        if linked:
            ign = Player(
                player=linked.uuid,
                requests_obj=mojang_session,
            ).name
            await interaction.edit_original_response(
                content=ERRORS["already_linked"].format(ign)
            )
            return

        uuid = await check_if_valid_ign(interaction, player)
        if not uuid:
            return

        integration = await IntegrationInfo.fetch(
            uuid=uuid,
            discord_id=interaction.user.id,
        )

        if (
            integration.discord_id in (None, 429, 500)
            or integration.player_uuid in (None, 429, 500)
        ):
            embed = Embed(
                title="Player Not Integrated To Voxyl Network",
                color=MAIN_COLOR,
                description=(
                    "To successfully link your account, please ensure that "
                    "you're using the correct IGN and Discord account that "
                    "is integrated to the Voxyl Network.\n\n"
                    "**Follow the steps below to integrate:**\n"
                    "- `1.` Join the official Bedwars Practice Discord "
                    "[here](https://discord.gg/7Mt7T8hqr4)\n"
                    "- `2.` Go to the integration channel\n"
                    "- `3.` Join `sync.voxyl.net` in Minecraft\n"
                    "- `4.` Copy the integration code shown in-game\n"
                    "- `5.` Run `;integrate <ign> <code>` in Discord\n"
                    "- `6.` After integration, run `/link <ign>` again\n"
                ),
            )
            await interaction.edit_original_response(embed=embed)
            return

        name = Player(
            player=integration.player_uuid,
            requests_obj=mojang_session,
        ).name

        if interaction.user.id == integration.discord_id:
            clean_uuid = integration.player_uuid.replace("-", "")
            LinkHandler(interaction.user.id).link_player(clean_uuid)
            await interaction.edit_original_response(
                content=f"You have successfully linked as **{name}**."
            )
            return

        await interaction.edit_original_response(
            content=ERRORS["integrated_to_other_account"].format(name, name)
        )

    except Exception as error:
        logger.error(error)
        await interaction.edit_original_response(
            content=ERRORS["application_error"]
        )


async def unlink_interaction(interaction: Interaction) -> None:
    try:
        linked = LinkHandler(interaction.user.id).get_linked_player()
        if not linked:
            await interaction.edit_original_response(
                content=ERRORS['account_not_linked']
            )
            return

        LinkHandler(interaction.user.id).unlink_player()
        await interaction.edit_original_response(
            content="You have been successfully unlinked."
        )

    except Exception as error:
        logger.error(error)
        await interaction.edit_original_response(
            content=ERRORS['application_error']
        )