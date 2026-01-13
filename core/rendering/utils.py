def get_role_prefix(role: str) -> str:
    role_prefixes = {
        "Owner": "&c[Owner] ",
        "Admin": "&c[Admin] ",
        "Manager": "&4[Manager] ",
        "Dev": "&a[Dev] ",
        "HeadBuilder": "&5[HeadBuilder] ",
        "Builder": "&d[Builder] ",
        "SrMod": "&e[SrMod] ",
        "Mod": "&e[Mod] ",
        "Trainee": "&a[Trainee] ",
        "Youtube": "&c[&fYoutube&c] ",
        "Master": "&6[Master] ",
        "Expert": "&9[Expert] ",
        "Adept": "&2[Adept] ",
        "Legend": "&6[Leg&een&fd&6] ",
    }
    return role_prefixes.get(role, "&7")


def get_displayname(name: str, role: str) -> str:
    if role == "Legend":
        if len(name) >= 3:
            name = '&6' + name[:-3] + '&e' + name[-3:-1] + '&f' + name[-1]
        elif len(name) == 2:
            name = '&6' + name[0] + '&6' + name[1]
        elif len(name) == 1:
            name = '&6' + name

    rank = get_role_prefix(role)

    return f"{rank}{name}"