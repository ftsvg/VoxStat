from discord import app_commands
from requests_cache import CachedSession


MAIN_COLOR: int = 0x5555FF

SESSION_CHOICES = [
    app_commands.Choice(name="1", value=1),
    app_commands.Choice(name="2", value=2),
    app_commands.Choice(name="3", value=3),
]

mojang_session = CachedSession(
    cache_name=f".cache/mojang", 
    expire_after=60
)