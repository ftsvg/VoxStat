from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import List

from discord import app_commands
from mcfetch import Player

from core import mojang_session


def get_xp_for_level(level: int) -> int:
    cycle = {
        0: 1000,
        1: 2000,
        2: 3000,
        3: 4000,
        4: 5000,
    }

    cycle_level = level % 100
    if cycle_level in cycle:
        return cycle[cycle_level]

    block = level // 100

    base_xp = 5000
    increment = 500

    if block <= 20:
        return base_xp + (block * increment)

    return base_xp + (20 * increment)


def format_difference(diff):
    if diff == 0:
        return "&a+0"
    
    color = "&a" if diff > 0 else "&c"
    sign = "+" if diff > 0 else "-"

    return f"{color}{sign}{abs(diff):,}"


def get_total_xp(level: int, partial_xp: int = 0) -> int:
    total_xp = 0
    for lvl in range(1, level):
        total_xp += get_xp_for_level(lvl)

    total_xp += partial_xp
    return total_xp


def get_xp_and_stars(
    old_level: int,
    old_xp: int,
    new_level: int,
    new_xp: int
) -> tuple[int, float]:
    
    old = get_total_xp(old_level, old_xp)
    new = get_total_xp(new_level, new_xp)

    xp_gained = new - old
    stars_gained = round(xp_gained / 5000, 2)

    return xp_gained, stars_gained


def started_on(unix_time: int) -> str:
    past = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    delta = relativedelta(now, past)

    if delta.years:
        ago = f"{delta.years} year{'s' if delta.years != 1 else ''} ago"
    elif delta.months:
        ago = f"{delta.months} month{'s' if delta.months != 1 else ''} ago"
    elif delta.days >= 7:
        weeks = delta.days // 7
        ago = f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif delta.days:
        ago = f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
    elif delta.hours:
        ago = f"{delta.hours} hr{'s' if delta.hours != 1 else ''} ago"
    elif delta.minutes:
        ago = f"{delta.minutes} min{'s' if delta.minutes != 1 else ''} ago"
    else:
        ago = f"{delta.seconds} sec{'s' if delta.seconds != 1 else ''} ago"

    date_formatted = past.strftime("%d/%m/%Y")
    return f"{date_formatted} ({ago})"


def resets_in(unix_time: int) -> str:
    future = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    if future <= now:
        return "resetting now"

    delta = relativedelta(future, now)

    if delta.years:
        remaining = f"in {delta.years} year{'s' if delta.years != 1 else ''}"
    elif delta.months:
        remaining = f"in {delta.months} month{'s' if delta.months != 1 else ''}"
    elif delta.days >= 7:
        weeks = delta.days // 7
        remaining = f"in {weeks} week{'s' if weeks != 1 else ''}"
    elif delta.days:
        remaining = f"in {delta.days} day{'s' if delta.days != 1 else ''}"
    elif delta.hours:
        remaining = f"in {delta.hours} hr{'s' if delta.hours != 1 else ''}"
    elif delta.minutes:
        remaining = f"in {delta.minutes} min{'s' if delta.minutes != 1 else ''}"
    else:
        remaining = f"in {delta.seconds} sec{'s' if delta.seconds != 1 else ''}"

    return remaining


PAGES: List[app_commands.Choice] = [
    app_commands.Choice(name=f"Page {i}", value=i) for i in range(1, 11)
]

def get_leaderboard_page(
    data: dict, 
    player: str
) -> tuple[int, int] | None:
    
    uuid = Player(player=player, requests_obj=mojang_session).uuid

    if not uuid:
        return None, None
    
    idx = next(
        (i for i, p in enumerate(data['players']) if str(p['uuid']).replace("-", "") == uuid)
    )

    if idx is None:
        return None, None
    
    page = idx // 10 + 1
    pos = idx % 10 + 1

    return page, pos
