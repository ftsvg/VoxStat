from requests_cache import CachedSession


MAIN_COLOR: int = 0x5555FF

mojang_session = CachedSession(
    cache_name=f".cache/mojang", 
    expire_after=60
)