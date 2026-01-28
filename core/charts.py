import time
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from core.api.helpers import GuildInfo


async def generate_xp_chart(
    x: list, 
    y: list, 
    colors: list, 
    last_updated: int, 
    guild_id: int, 
    high_quality=False
):
    data = sorted(
        zip(x, y, colors), 
        key=lambda item: item[1], 
        reverse=True
    )

    x, y, colors = map(list, zip(*data))

    colors[0] = "#2ecc71"
    colors[1:5] = ["#1f8b4c"] * 4

    plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")
    if high_quality:
        plt.figure(figsize=(16, 6), dpi=300)
    else:
        plt.figure(figsize=(16, 6))
    plt.margins(x=0.01)

    bars = plt.bar(x, y, edgecolor="black", linewidth=1.5, color=colors)
    plt.bar_label(bars, fontsize=13, rotation=90, padding=10, fmt="%.1f")

    best_patch = mpatches.Patch(facecolor="#2ecc71", edgecolor="white", label="#1 Stars", linewidth=2)
    top_5_patch = mpatches.Patch(facecolor="#1f8b4c", edgecolor="white", label="Top 5 stars", linewidth=2)
    good_patch = mpatches.Patch(facecolor="#1685F8", edgecolor="white", label=">= 2 stars")
    bad_patch = mpatches.Patch(facecolor="#F32C55", edgecolor="white", label="< 2 Stars")

    plt.legend(
        handles=[
            best_patch, top_5_patch, good_patch, bad_patch
        ], 
        loc="upper right", 
        fontsize=16
    )

    today = int(time.time())
    guild_data = await GuildInfo.fetch(guild_id)

    if last_updated is None:
        last_updated = int(datetime.now().timestamp())

    old_date = datetime.fromtimestamp(last_updated).strftime("%B %d")
    today = datetime.now().strftime("%B %d")

    plt.figtext(0.5, 0.95, f"{guild_data.name} XP Chart", fontsize=25, ha="center", fontweight="bold")
    plt.figtext(0.5, 0.9, f"{old_date} - {today}", fontsize=16, ha="center")
    plt.figtext(0.85, 0.9, f"Total Stars: {round(sum(y))}", fontsize=16, ha="center")

    plt.xticks(fontsize=14, rotation=90)

    plt.savefig(
        f"./assets/charts/xp_chart.png", bbox_inches="tight", pad_inches=0.25
    )
    plt.close()