from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo

from core import mojang_session, calc_projected, format_difference
from database import Session
from core.rendering import get_displayname, get_prestige_color


async def render_projected(
    uuid: str, 
    stats: PlayerInfo,
    session: Session,
    target_level: int
) -> None:
    
    path = f"./assets/bg/projected/base.png"
    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    data = calc_projected(
        target_level=target_level,
        session=session,
        current=stats
    )

    if "error" in data:
        return data["error"]

    ign = Player(player=uuid, requests_obj=mojang_session).name
    display_name = get_displayname(ign, stats.role)

    cur_level = get_prestige_color(stats.level)
    new_level = get_prestige_color(target_level)

    im.text.draw_many([
        (f'{cur_level} {display_name}', {'position': (410, 50), "align": "center", "font_size": 20}),

        (f'&fWins', {'position': (160, 140), "align": "center", "font_size": 14}),
        (f'&fWeighted Wins', {'position': (410, 140), "align": "center", "font_size": 14}),
        (f'&fLevel', {'position': (660, 140), "align": "center", "font_size": 14}),
        (f'&fKills', {'position': (160, 245), "align": "center", "font_size": 14}),
        (f'&fFinals', {'position': (410, 245), "align": "center", "font_size": 14}),
        (f'&fBeds', {'position': (660, 245), "align": "center", "font_size": 14}),

        (f'&a{stats.wins:,} &f➡ &a{data["wins"]:,}', {'position': (160, 162), "align": "center", "font_size": 18}),
        (f'&c{stats.weightedwins:,} &f➡ &c{data["weightedwins"]:,}', {'position': (410, 162), "align": "center", "font_size": 18}),
        (f'{cur_level} &f➡ {new_level}', {'position': (660, 162), "align": "center", "font_size": 18}),
        (f'&9{stats.kills:,} &f➡ &9{data["kills"]:,}', {'position': (160, 267), "align": "center", "font_size": 18}),
        (f'&d{stats.finals:,} &f➡ &d{data["finals"]:,}', {'position': (410, 267), "align": "center", "font_size": 18}),
        (f'&e{stats.beds:,} &f➡ &e{data["beds"]:,}', {'position': (660, 267), "align": "center", "font_size": 18}),

        (f'{format_difference(data["wins"] - stats.wins)}', {"position": (160, 203), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(data["weightedwins"] - stats.weightedwins)}', {"position": (410, 203), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(target_level - stats.level)}', {"position": (660, 203), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(data["kills"] - stats.kills)}', {"position": (160, 308), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(data["finals"] - stats.finals)}', {"position": (410, 308), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(data["beds"] - stats.beds)}', {"position": (660, 308), 'align': 'center',  'font_size': 14}),

        (f'&7Projected to hit {new_level} &7on &f{data["projected_date"]}', {"position": (410, 352), 'align': 'center',  'font_size': 16}),

        ("&fProjected Stats (Overall)", {"position": (410, 98), 'align': 'center',  'font_size': 14}),
        ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (410, 398), 'align': 'center',  'font_size': 14})
    ],
        {"shadow_offset": (2, 2)} 
    )

    im.save(f"./assets/stats/projected.png")

