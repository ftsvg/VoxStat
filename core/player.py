from typing import Optional

from discord import Interaction
from mcfetch import Player

from content import ERRORS
from core.api.helpers import PlayerInfo
from database.handlers import LinkHandler
from core import mojang_session


async def check_if_ever_played(
    interaction: Interaction,
    uuid: str,
) -> bool:
    if not uuid:
        return False

    player = await PlayerInfo.fetch(uuid)
    last_login = player.last_login_time

    if last_login == 429:
        await interaction.edit_original_response(
            content=ERRORS['rate_limited']
        )
        return False

    if last_login == 500:
        await interaction.edit_original_response(
            content=ERRORS['failed_to_fetch']
        )
        return False

    if last_login is None:
        await interaction.edit_original_response(
            content=ERRORS['never_played']
        )
        return False

    return True


async def check_if_linked(
    interaction: Interaction,
    player: Optional[str],
) -> Optional[str]:
    if player is None:
        linked = LinkHandler(interaction.user.id).get_linked_player()

        if linked:
            player = Player(
                player=linked.uuid,
                requests_obj=mojang_session,
            ).name

        if not player:
            await interaction.edit_original_response(
                content=ERRORS['not_linked']
            )
            return None

    return player


async def check_if_linked_discord(
    interaction: Interaction,
    message: Optional[str] = None,
) -> Optional[str]:
    if not message:
        message = ERRORS['not_linked']

    linked = LinkHandler(interaction.user.id).get_linked_player()
    if not linked:
        await interaction.edit_original_response(content=message)
        return None

    return linked.uuid


async def not_exist_message(
    interaction: Interaction,
    player: str,
) -> None:
    
    await interaction.edit_original_response(
        content=ERRORS['invalid_player'].format(player)
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
            content=ERRORS['api_down']
        )
        return None