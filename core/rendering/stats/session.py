from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo
from database import Session
from database.handlers import SessionHandler

from core import get_xp_and_stars, started_on, mojang_session

from core.rendering import get_displayname, get_progress_bar, render_skin


async def render_session(uuid: str, session: int) -> None:
    path = f"./assets/bg/sessions/base.png"
    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    player = await PlayerInfo.fetch(uuid)
    ign = Player(
        player=uuid, requests_obj=mojang_session
    ).name

    session_data: Session = SessionHandler(uuid, session).get_session()
    if not session_data:
        return None

    im.text.draw_many([
        (f'&fWins', {'position': (404, 185), "align": "center", "font_size": 16}),
        (f'&fWeighted Wins', {'position': (649, 185), "align": "center", "font_size": 16}),

        (f'&fKills', {'position': (363, 265), "align": "center", "font_size": 16}),
        (f'&fFinals', {'position': (526, 265), "align": "center", "font_size": 16}),
        (f'&fBeds', {'position': (690, 265), "align": "center", "font_size": 16}),

        (f'&fLevels Gained', {'position': (404, 340), "align": "center", "font_size": 16}),
        (f'&fEXP Gained', {'position': (649, 340), "align": "center", "font_size": 16}),
        
        (f'&fBWP Stats (Overall)', {'position': (631, 138), "align": "center", "font_size": 14}),
        (f'&fSession &8(&7#{session}&8)', {'position': (386, 138), "align": "center", "font_size": 14}),
    ],
        {"shadow_offset": (2, 2)} 
    )

    wins = int(player.wins) - int(session_data.wins)
    weighted = int(player.weightedwins) - int(session_data.weighted)
    kills = int(player.kills) - int(session_data.kills)
    finals = int(player.finals) - int(session_data.finals)
    beds = int(player.beds) - int(session_data.beds)

    exp_gained, stars_gained = get_xp_and_stars(
        old_level=int(session_data.star),
        old_xp=int(session_data.xp),
        new_level=int(player.level),
        new_xp=int(player.exp)
    )

    display_name = get_displayname(ign, player.role)
    parts = await get_progress_bar(player.level, player.exp)

    started = started_on(session_data.start_time)

    im.text.draw_many([
        (f'&a{wins:,}', {'position': (404, 207), "align": "center", "font_size": 20}),
        (f'&9{weighted:,}', {'position': (649, 207), "align": "center", "font_size": 20}),

        (f'&d{kills:,}', {'position': (363, 287), "align": "center", "font_size": 20}),
        (f'&c{finals:,}', {'position': (526, 287), "align": "center", "font_size": 20}),
        (f'&e{beds:,}', {'position': (690, 287), "align": "center", "font_size": 20}),

        (f'&b{stars_gained}', {'position': (404, 362), "align": "center", "font_size": 18}),
        (f'&b{exp_gained:,}', {'position': (649, 362), "align": "center", "font_size": 18}),

        (f'{display_name}', {'position': (526, 50), "align": "center", "font_size": 20}),

        (f'{parts[0]}',   {'position': (446, 413), 'align': 'right',   'font_size': 16}),
        (f'{parts[1]}', {'position': (526, 411), 'align': 'center', 'font_size': 16}),
        (f'{parts[2]}',  {'position': (609, 413), 'align': 'left',  'font_size': 16}),

        (f'Started {started}',  {'position': (526, 98), 'align': 'center',  'font_size': 14}),
        ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (525, 458), 'align': 'center',  'font_size': 14})
    ],
        {"shadow_offset": (2, 2)} 
    )

    await render_skin(
        image=im._image, 
        uuid=uuid, 
        position=(55, 95),
        size=(204, 374),
        style='full'
    )
    im.save(f"./assets/stats/session.png")