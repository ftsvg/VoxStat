from typing import List

from core import get_xp_for_level
from core.rendering import get_prestige_color


async def get_progress_bar(
    level: int,
    xp: int
) -> List[str]:
    progress_symbol = "⏹"
    progress_bar_max = 10

    xp_needed = get_xp_for_level(level)

    if xp is None or xp <= 0 or xp_needed is None:
        xp_needed = 5000
        bar = f"&7{progress_symbol * progress_bar_max}"
    else:
        ratio = xp / xp_needed
        colored_chars = max(1, int(progress_bar_max * ratio))
        colored_chars = min(colored_chars, progress_bar_max)
        gray_chars = progress_bar_max - colored_chars

        colored_progress = f"&b{progress_symbol * colored_chars}"
        gray_progress = f"&7{progress_symbol * gray_chars}"

        bar = colored_progress + gray_progress

    new_level = int(level + 1)

    cur_level = get_prestige_color(level)
    next_level = get_prestige_color(new_level)

    return [
        f"{cur_level} &8[",
        f"{bar}",
        f"&8] {next_level}"
    ]