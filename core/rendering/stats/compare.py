from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo
from core import mojang_session, format_difference
from core.rendering import get_displayname, get_prestige_color


async def render_compare(
    player_1_uuid: str, 
    player_2_uuid: str
) -> None:
    
    path = f"./assets/bg/compare/base.png"
    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    player_1_ign = Player(player=player_1_uuid, requests_obj=mojang_session).name
    player_2_ign = Player(player=player_2_uuid, requests_obj=mojang_session).name

    p1 = await PlayerInfo.fetch(player_1_uuid)
    p2 = await PlayerInfo.fetch(player_2_uuid)

    display_name_1 = get_displayname(player_1_ign, p1.role)
    display_name_2 = get_displayname(player_2_ign, p2.role)

    p1_level = get_prestige_color(p1.level)
    p2_level = get_prestige_color(p2.level)

    im.text.draw_many([
        (f'{display_name_1}', {'position': (410, 50), "align": "center", "font_size": 20}),
        (f'{display_name_2}', {'position': (410, 95), "align": "center", "font_size": 20}),

        (f'&fWins', {'position': (160, 147), "align": "center", "font_size": 14}),
        (f'&fWeighted Wins', {'position': (410, 147), "align": "center", "font_size": 14}),
        (f'&fLevel', {'position': (660, 147), "align": "center", "font_size": 14}),
        (f'&fKills', {'position': (160, 252), "align": "center", "font_size": 14}),
        (f'&fFinals', {'position': (410, 252), "align": "center", "font_size": 14}),
        (f'&fBeds', {'position': (660, 252), "align": "center", "font_size": 14}),

        (f'&a{p1.wins:,} &7/ &a{p2.wins:,}', {'position': (160, 165), "align": "center", "font_size": 18}),
        (f'&c{p1.weightedwins:,} &7/ &c{p2.weightedwins:,}', {'position': (410, 165), "align": "center", "font_size": 18}),
        (f'{p1_level} &7/ {p2_level}', {'position': (660, 165), "align": "center", "font_size": 18}),
        (f'&9{p1.kills:,} &7/ &9{p2.kills:,}', {'position': (160, 270), "align": "center", "font_size": 18}),
        (f'&d{p1.finals:,} &7/ &d{p2.finals:,}', {'position': (410, 270), "align": "center", "font_size": 18}),
        (f'&e{p1.beds:,} &7/ &e{p2.beds:,}', {'position': (660, 270), "align": "center", "font_size": 18}),

        (f'{format_difference(p1.wins - p2.wins)}', {"position": (160, 208), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(p1.weightedwins - p2.weightedwins)}', {"position": (410, 208), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(p1.level - p2.level)}', {"position": (660, 208), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(p1.kills - p2.kills)}', {"position": (160, 313), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(p1.finals - p2.finals)}', {"position": (410, 313), 'align': 'center',  'font_size': 14}),
        (f'{format_difference(p1.beds - p2.beds)}', {"position": (660, 313), 'align': 'center',  'font_size': 14}),
        
        ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (410, 353), 'align': 'center',  'font_size': 14})
    ],
        {"shadow_offset": (2, 2)} 
    )

    im.save(f"./assets/stats/compare.png")

