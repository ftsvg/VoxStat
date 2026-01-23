from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from database import HistoricalStats
from database.handlers import HistoricalHandler

from core import get_xp_and_stars, resets_in, mojang_session
from core.api.helpers import PlayerInfo
from core.rendering import get_displayname, get_progress_bar, render_skin


async def render_historical(
    player: PlayerInfo,
    uuid: str, 
    period: str,
    reset: int
) -> None:

    path = f"./assets/bg/historical/base.png"
    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    ign = Player(
        player=uuid, requests_obj=mojang_session
    ).name

    historical_data: HistoricalStats = HistoricalHandler(uuid, period).get_stats()
    if not historical_data:
        return None

    im.text.draw_many([
        (f'&fWins', {'position': (404, 185), "align": "center", "font_size": 16}),
        (f'&fWeighted Wins', {'position': (649, 185), "align": "center", "font_size": 16}),

        (f'&fFinal Kills', {'position': (363, 265), "align": "center", "font_size": 16}),
        (f'&fKills', {'position': (526, 265), "align": "center", "font_size": 16}),
        (f'&fBeds Broken', {'position': (690, 265), "align": "center", "font_size": 16}),

        (f'&fLevels Gained', {'position': (404, 340), "align": "center", "font_size": 16}),
        (f'&fEXP Gained', {'position': (649, 340), "align": "center", "font_size": 16}),
        
        (f'&fBWP Stats ({period.title()})', {'position': (631, 138), "align": "center", "font_size": 14}),
        (f'&fHistorical stats', {'position': (386, 138), "align": "center", "font_size": 14}),
    ],
        {"shadow_offset": (2, 2)} 
    )

    wins = int(player.wins - historical_data.wins)
    weighted = int(player.weightedwins - historical_data.weighted) 
    kills = int(player.kills - historical_data.kills) 
    finals = int(player.finals - historical_data.finals)
    beds = int(player.beds - historical_data.beds)

    exp_gained, stars_gained = get_xp_and_stars(
        old_level = historical_data.level,
        old_xp = historical_data.xp,
        new_level = player.level,
        new_xp = player.exp
    )

    display_name = get_displayname(ign, player.role)
    parts = await get_progress_bar(player.level, player.exp)

    im.text.draw_many([
        (f'&a{wins:,}', {'position': (404, 207), "align": "center", "font_size": 20}),
        (f'&9{weighted:,}', {'position': (649, 207), "align": "center", "font_size": 20}),

        (f'&d{finals:,}', {'position': (363, 287), "align": "center", "font_size": 20}),
        (f'&c{kills:,}', {'position': (526, 287), "align": "center", "font_size": 20}),
        (f'&e{beds:,}', {'position': (690, 287), "align": "center", "font_size": 20}),

        (f'&b{stars_gained}', {'position': (404, 362), "align": "center", "font_size": 18}),
        (f'&b{exp_gained:,}', {'position': (649, 362), "align": "center", "font_size": 18}),

        (f'{display_name}', {'position': (526, 50), "align": "center", "font_size": 20}),

        (f'{parts[0]}',   {'position': (446, 413), 'align': 'right',   'font_size': 16}),
        (f'{parts[1]}', {'position': (526, 411), 'align': 'center', 'font_size': 16}),
        (f'{parts[2]}',  {'position': (609, 413), 'align': 'left',  'font_size': 16}),

        (f'Next reset {resets_in(reset)}',  {'position': (526, 98), 'align': 'center',  'font_size': 14}),
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
    im.save(f"./assets/stats/historical.png")