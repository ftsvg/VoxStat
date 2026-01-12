"""from typing import Optional

from discord import Interaction
from mcfetch import Player

from voxlib.api.utils import PlayerInfo
from voxlib.database.utils import Linking
from voxlib import mojang_session


async def check_if_ever_played(
    interaction: Interaction,
    uuid: str,
) -> bool:
    if not uuid:
        return False

    player = PlayerInfo(uuid)
    last_login = await player.last_login_time

    if last_login == 429:
        await interaction.edit_original_response(
            content="We are being rate limited. Please try again later."
        )
        return False

    if last_login == 500:
        await interaction.edit_original_response(
            content="Failed to fetch player data."
        )
        return False

    if last_login is None:
        await interaction.edit_original_response(
            content=(
                "This player has never played on "
                "`bedwarspractice.club` before!"
            )
        )
        return False

    return True


async def check_if_linked(
    interaction: Interaction,
    player: Optional[str],
) -> Optional[str]:
    if player is None:
        linked = Linking(interaction.user.id).get_linked_player()

        if linked:
            player = Player(
                player=linked[1],
                requests_obj=mojang_session,
            ).name

        if not player:
            await interaction.edit_original_response(
                content=(
                    "You are not linked! Either specify a player "
                    "or link your account using `/link`"
                )
            )
            return None

    return player


async def check_if_linked_discord(
    interaction: Interaction,
    message: Optional[str] = None,
) -> Optional[str]:
    if not message:
        message = (
            "You are not linked! Either specify a player "
            "or link your account using `/link`"
        )

    linked = Linking(interaction.user.id).get_linked_player()
    if not linked:
        await interaction.edit_original_response(content=message)
        return None

    return linked[1]


async def not_exist_message(
    interaction: Interaction,
    player: str,
) -> None:
    await interaction.edit_original_response(
        content=(
            f"**{player}** does not exist! "
            "Please provide a valid username."
        )
    )


async def check_if_valid_ign(
    interaction: Interaction,
    player: str,
) -> Optional[str]:
    if len(player) > 16:
        await not_exist_message(interaction, player)
        return None

    uuid = Player(
        player=player,
        requests_obj=mojang_session,
    ).uuid

    if uuid is None:
        await not_exist_message(interaction, player)
        return None

    return uuid


async def fetch_player(
    interaction: Interaction,
    player: Optional[str],
) -> Optional[str]:
    try:
        if not (player := await check_if_linked(interaction, player)):
            return None

        if not (uuid := await check_if_valid_ign(interaction, player)):
            return None

        if not await check_if_ever_played(interaction, uuid):
            return None

        return uuid

    except Exception:
        await interaction.edit_original_response(
            content=(
                "The API is currently down. If this issue persists, "
                "please contact the **VoxStats Dev Team**."
            )
        )
        return None"""