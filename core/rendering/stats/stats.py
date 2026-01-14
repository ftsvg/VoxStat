from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo
from core.rendering import get_displayname, render_skin, get_progress_bar, get_prestige_color
from core import MODE_CONFIG, STAT_LAYOUTS, mojang_session, get_xp_for_level
from logger import logger


def resolve_stat_type(config: dict, view: str) -> str:
    return config.get("types", {}).get(view, "Overall")


def resolve_stats(player: PlayerInfo, joins: tuple[str | None, str | None], view: str) -> dict:
    single, double = joins
    stats = player.game_stats.get("stats", {})

    if view == "single" and single:
        return stats.get(single, {})

    if view == "double" and double:
        return stats.get(double, {})

    if view == "combined":
        if single and double:
            s = stats.get(single, {})
            d = stats.get(double, {})
            return {k: s.get(k, 0) + d.get(k, 0) for k in s.keys() | d.keys()}
        if single:
            return stats.get(single, {})

    return {}


async def render_overall(player: PlayerInfo, uuid: str):
    path = "./assets/bg/stats/base.png"
    bg = BackgroundImageLoader(path)
    im = ImageRender(bg.load_image(path).convert("RGBA"))

    values = {
        "wins": player.wins,
        "weighted": player.weightedwins,
        "kills": player.kills,
        "finals": player.finals,
        "beds": player.beds
    }

    for key, pos, color, font_size in STAT_LAYOUTS[5]:
        if key.islower():
            value = values.get(key, 0)
            text = f"{color}{value:,}"
        else:
            text = f"{color}{key}"

        im.text.draw_many(
            [(text, {"position": pos})],
            default_text_options={
                "shadow_offset": (2, 2),
                "align": "center",
                "font_size": font_size
            }
        )

    ign = Player(player=uuid, requests_obj=mojang_session).name
    display_name = get_displayname(ign, player.role)

    parts = await get_progress_bar(player.level, player.exp)
    cur_level = get_prestige_color(player.level)
    xp_next_level = get_xp_for_level(player.level)

    im.text.draw_many(
        [
            ("&fOverall Stats", {"position": (525, 218)}),
            ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (525, 418)}),
            (display_name, {"position": (525, 50), "align": "center", "font_size": 20}),
            (f"&7Level: {cur_level}", {"position": (525, 112), "align": "center", "font_size": 16}),
            (f"&7Exp progress: &b{player.exp:,}&8 / &a{xp_next_level:,}", {"position": (525, 136), "align": "center", "font_size": 16}),
            (parts[0], {"position": (436, 160), "align": "right", "font_size": 18}),
            (parts[1], {"position": (525, 158), "align": "center", "font_size": 18}),
            (parts[2], {"position": (617, 160), "align": "left", "font_size": 18}),
        ],
        default_text_options={
            "shadow_offset": (2, 2),
            "align": "center",
            "font_size": 14
        }
    )

    await render_skin(
        image=im._image,
        uuid=uuid,
        position=(55, 60),
        size=(204, 374),
        style="full"
    )

    im.save("./assets/stats/stats.png")


async def render_generic(mode: str, data: dict, total_stats: int, stat_type: str, uuid: str, player: PlayerInfo):
    path = f"./assets/bg/stats/stats_{total_stats}/base.png"
    bg = BackgroundImageLoader(path)
    im = ImageRender(bg.load_image(path).convert("RGBA"))

    for key, pos, color, font_size in STAT_LAYOUTS[total_stats]:
        if key.islower():
            value = data.get(key, 0)
            text = f"{color}{value:,}"
        else:
            text = f"{color}{key}"

        im.text.draw_many(
            [(text, {"position": pos})],
            default_text_options={
                "shadow_offset": (2, 2),
                "align": "center",
                "font_size": font_size
            }
        )

    ign = Player(player=uuid, requests_obj=mojang_session).name
    display_name = get_displayname(ign, player.role)

    parts = await get_progress_bar(player.level, player.exp)
    cur_level = get_prestige_color(player.level)
    xp_next_level = get_xp_for_level(player.level)

    im.text.draw_many(
        [
            (f"&f{mode} ({stat_type}) Stats", {"position": (525, 218)}),
            ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (525, 418)}),
            (display_name, {"position": (525, 50), "align": "center", "font_size": 20}),
            (f"&7Level: {cur_level}", {"position": (525, 112), "align": "center", "font_size": 16}),
            (f"&7Exp progress: &b{player.exp:,}&8 / &a{xp_next_level:,}", {"position": (525, 136), "align": "center", "font_size": 16}),
            (parts[0], {"position": (436, 160), "align": "right", "font_size": 18}),
            (parts[1], {"position": (525, 158), "align": "center", "font_size": 18}),
            (parts[2], {"position": (617, 160), "align": "left", "font_size": 18}),
        ],
        default_text_options={
            "shadow_offset": (2, 2),
            "align": "center",
            "font_size": 14
        }
    )

    await render_skin(
        image=im._image,
        uuid=uuid,
        position=(55, 60),
        size=(204, 374),
        style="full"
    )

    im.save("./assets/stats/stats.png")


async def render_stats(mode: str, uuid: str, view: str = "combined"):
    try:
        config = MODE_CONFIG.get(mode)
        player = await PlayerInfo.fetch(uuid)

        if config.get("overall"):
            return await render_overall(player, uuid)

        data = resolve_stats(player, config["joins"], view)
        stat_type = resolve_stat_type(config, view)

        await render_generic(mode, data, config["stats"], stat_type, uuid, player)

    except Exception as error:
        logger.error(error)
