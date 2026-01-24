from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo

from core import mojang_session

from core.rendering import get_displayname, get_prestige_color, render_skin


async def render_leaderboard(
    data: dict,
    page: int,
    pos: int = None,
    lb_type: str = "level"
) -> None:
    
    if pos:
        path = f"./assets/bg/leaderboard/hl/{pos}.png"
    else:
        path = f"./assets/bg/leaderboard/base.png"

    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    start_idx = (page - 1) * 10
    end_idx = start_idx + 10

    y = 133
    y_skin = 132

    if lb_type.lower() == "weightedwins":
        lb_type = "Weighted Wins"

    im.text.draw_many([
        (f"&f{lb_type} Leaderboard", {"position": (400, 48), 'align': 'center',  'font_size': 14}),
        ("&fPos", {"position": (75, 88), 'align': 'center',  'font_size': 18}),
        ("&fPlayers", {"position": (350, 88), 'align': 'center',  'font_size': 18}),
        (f"&f{lb_type}", {"position": (675, 88), 'align': 'center',  'font_size': 18}),

        ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (400, 583), 'align': 'center',  'font_size': 14})
    ],
        {"shadow_offset": (2, 2)} 
    )   

    for idx, player in enumerate(data['players'][start_idx:end_idx], start=start_idx+1):
        pos = str(idx)
        color = {
            "1": "&e",
            "2": "&7",
            "3": "&6"
        }.get(pos, "&f")

        im.text.draw(f"{color}#{pos}", text_options={
            "position": (75, y), "font_size": 18, "shadow_offset": (2, 2), "align": "center"
            }
        )
        
        uuid = str(player['uuid']).replace("-", "")
        stats = await PlayerInfo.fetch(uuid)

        ign = Player(player=uuid, requests_obj=mojang_session).name

        display_name = get_displayname(ign, stats.role)
        prestige = get_prestige_color(stats.level)

        stat = stats.level if lb_type.lower() == "level" else stats.weightedwins

        im.text.draw_many([
            (f"{prestige} {display_name}", {"position": (160, y), 'align': 'left',  'font_size': 18}),
            (f"&f{stat:,}", {"position": (675, y), 'align': 'center',  'font_size': 18}),
        ],
            {"shadow_offset": (2, 2)} 
        )   

        await render_skin(
            image=im._image,
            uuid=uuid,
            position=(130, y_skin),
            size=(20, 20),
            style="face"
        )   
        y += 45
        y_skin += 45

    if lb_type.lower() == "weighted wins": lb_type = "weightedwins" 
    im.save(f"./assets/stats/leaderboard_{lb_type.lower()}.png")

