from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo
from core.rendering import get_displayname, render_skin
from core import MODE_CONFIG, STAT_LAYOUTS, mojang_session
from logger import logger


def resolve_stat_type(config: dict, view: str) -> str:
    return config.get("types", {}).get(view, "Overall")


def resolve_stats(
    player: PlayerInfo,
    joins: tuple[str | None, str | None],
    view: str
) -> dict:
    single, double = joins

    stats = (
        player.game_stats.get("stats", {})
        if isinstance(player.game_stats, dict)
        else {}
    )

    if view == "single" and single:
        return stats.get(single, {})

    if view == "double" and double:
        return stats.get(double, {})

    if view == "combined" and single and double:
        s: dict = stats.get(single, {})
        d: dict = stats.get(double, {})
        return {k: s.get(k, 0) + d.get(k, 0) for k in s.keys() | d.keys()}

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
        if key in values:
            text = f"{color}{values[key]:,}"
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

    im.text.draw_many(
        [(f"&fOverall Stats", {"position": (525, 218)}),
        (f"&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (525, 418)}),
        (f"{display_name}", {'position': (525, 50), "align": "center", "font_size": 20})
    ],
        default_text_options={
            "shadow_offset": (2, 2), "align": "center", "font_size": 14
        }
    )

    await render_skin(
        image=im._image, 
        uuid=uuid, 
        position=(55, 60),
        size=(204, 374),
        style='full'
    )

    im.save("./assets/stats/stats.png")


async def render_generic(
    mode: str,
    data: dict,
    total_stats: int,
    stat_type: str,
    uuid: str,
    role: str
):
    path = f"./assets/bg/stats/stats_{total_stats}/base.png"
    bg = BackgroundImageLoader(path)
    im = ImageRender(bg.load_image(path).convert("RGBA"))

    for key, pos, color, font_size in STAT_LAYOUTS[total_stats]:
        if key in data:
            text = f"{color}{data[key]:,}"
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
    display_name = get_displayname(ign, role)

    im.text.draw_many(
        [(f"&f{mode} ({stat_type}) Stats", {"position": (525, 218)}),
        (f"&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (525, 418)}),
        (f"{display_name}", {'position': (525, 50), "align": "center", "font_size": 20})
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
        style='full'
    )

    im.save("./assets/stats/stats.png")


async def render_stats(
    mode: str,
    uuid: str,
    view: str = "combined"
):
    try:
        config = MODE_CONFIG.get(mode)

        player = await PlayerInfo.fetch(uuid)

        if config.get("overall"):
            return await render_overall(player, uuid)

        data = resolve_stats(player, config["joins"], view)
        stat_type = resolve_stat_type(config, view)

        await render_generic(
            mode, data, config["stats"], stat_type, uuid, player.role
        )

    except Exception as error:
        logger.error(error)