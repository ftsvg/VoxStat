from os import getenv

from dotenv import load_dotenv

from content import SETTINGS_ERRORS

load_dotenv()


class Settings:
    TOKEN: str = getenv("TOKEN")
    
    DBUSER: str = getenv("DBUSER")
    DBPASS: str = getenv("DBPASS")
    DBNAME: str = getenv("DBNAME")
    DBPORT: int = int(getenv("DBPORT"))
    DBENDPOINT: str = getenv("DBENDPOINT")

    API_KEY: str = getenv("API_KEY")
    BASE_URL: str = "https://api.voxyl.net"

    SUPPORT_SERVER: str = getenv("SUPPORT_SERVER")

    SUGGESTIONS_CHANNEL: int = int(getenv("SUGGESTIONS_CHANNEL"))
    BUG_CHANNEL: int = int(getenv("BUG_CHANNEL"))

    @classmethod
    def validate(cls) -> None:
        if not cls.TOKEN:
            raise RuntimeError(SETTINGS_ERRORS['missing_token'])
        
        if not all([cls.DBUSER, cls.DBPASS, cls.DBNAME, cls.DBENDPOINT]):
            raise RuntimeError(SETTINGS_ERRORS['missing_database_credentials'])
        
        if not cls.API_KEY:
            raise RuntimeError(SETTINGS_ERRORS['missing_voxyl_api_key'])