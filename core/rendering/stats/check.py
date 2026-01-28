import json

from mctextrender import BackgroundImageLoader, ImageRender
from mcfetch import Player

from core.api.helpers import PlayerInfo
from database import Users

from core import get_stars_gained, mojang_session

from core.rendering import get_displayname, get_prestige_color, render_skin


async def render_check(uuid: str, user_data: Users) -> None:
    path = f"./assets/bg/check/base.png"
    bg = BackgroundImageLoader(path)
    base_img = bg.load_image(path).convert("RGBA")
    im = ImageRender(base_img)

    player = await PlayerInfo.fetch(uuid)
    ign = Player(player=uuid, requests_obj=mojang_session).name
    
    highest_week = user_data.highest_star
    past_star_weeks = user_data.past_star_weeks
    past_star_weeks = json.loads(past_star_weeks)
    average_star = round(sum(past_star_weeks) / len(past_star_weeks), 2)

    display_name = get_displayname(ign, player.role)

    level = get_prestige_color(user_data.star)
    new_level = player.level
    new_xp = player.exp

    stars_gained = get_stars_gained(
        user_data.star, user_data.xp, new_level, new_xp
    )

    im.text.draw_many([
        (f'{display_name}', {'position': (435, 50), "align": "center", "font_size": 20}),

        (f'&7Current Week Stats', {'position': (435, 98), "align": "center", "font_size": 14}),

        (f'&fStart Level', {'position': (315, 140), "align": "center", "font_size": 14}),
        (f'{level}', {'position': (315, 162), "align": "center", "font_size": 18}),
        
        (f'&fStars Gained', {'position': (555, 140), "align": "center", "font_size": 14}),
        (f'&b{round(stars_gained, 2)}✫', {'position': (555, 162), "align": "center", "font_size": 18}),

        (f'&7Past 5 Weeks', {'position': (355, 210), "align": "center", "font_size": 14}),
        (f'&fRecent Week ➡ Oldest Week', {'position': (355, 230), "align": "center", "font_size": 14}),

        (f'&7Overall Statistics', {'position': (355, 343), "align": "center", "font_size": 14}),
        (f'&fAverage Stars / Week', {'position': (195, 385), "align": "center", "font_size": 14}),
        (f'&e{average_star}✫', {'position': (195, 407), "align": "center", "font_size": 18}),

        (f'&fHighest Stars in a Week', {'position': (515, 385), "align": "center", "font_size": 14}),
        (f'&d{highest_week}✫', {'position': (515, 407), "align": "center", "font_size": 18}),

        ("&7Made with &c❤ &7by &9VoxStat's &7developers", {"position": (355, 453), 'align': 'center',  'font_size': 14})
    ],
        {"shadow_offset": (2, 2)}
    )

    x = 99
    for week in past_star_weeks:
        if week < 1:
            color = "&c"
        elif week < 2:
            color = "&6"
        else:
            color = "&a"

        im.text.draw(f"{color}{week}✫", text_options={
            "position": (x, 285), "font_size": 20, "shadow_offset": (2, 2), "align": "center"
            }
        )
        x += 128
        
    await render_skin(
        image=im._image,
        uuid=uuid,
        position=(55, 40),
        size=(120, 150),
        style="bust"
    )

    im.save(f"./assets/stats/check.png")