class PrestigeColorMaps:
    prestige_map = {
        900: '&5',
        800: '&9',
        700: '&d',
        600: '&4',
        500: '&3',
        400: '&2',
        300: '&b',
        200: '&6',
        100: '&f',
        0: '&7',
    }


    prestige_map_2 = {
        1100: ("&7", "&f", "&f", "&f", "&f", "&7", "&7"),
        1000: ("&c", "&6", "&e", "&a", "&b", "&d", "&5")
    }



def get_prestige_color(level: int) -> str:
    c = PrestigeColorMaps
    level_str = f"[{level}✫]"

    if level < 1000:
        for threshold in sorted(c.prestige_map.keys(), reverse=True):
            if level >= threshold:
                color = c.prestige_map[threshold]
                return "".join(f"{color}{char}" for char in level_str)

    for threshold in sorted(c.prestige_map_2.keys(), reverse=True):
        if level >= threshold:
            colors = c.prestige_map_2[threshold]
            return "".join(
                f"{colors[i % len(colors)]}{char}" for i, char in enumerate(level_str)
            )

    return "".join(f"&7{char}" for char in level_str)