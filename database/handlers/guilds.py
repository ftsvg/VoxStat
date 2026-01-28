from database import ensure_cursor, Cursor, Guilds


class GuildsHandler:
    def __init__(self, guild_id: int | None = None):
        self.guild_id: int = guild_id


    @ensure_cursor
    def get_all_guilds(self, *, cursor: Cursor = None) -> list[Guilds] | None:
        cursor.execute("SELECT * FROM guilds")
        rows = cursor.fetchall()
        
        return [Guilds(**row) for row in rows] if rows else [] 


    @ensure_cursor
    def get_guild(self, *, cursor: Cursor = None) -> Guilds | None:
        cursor.execute(
            "SELECT * FROM guilds WHERE guild_id=%s",
            (self.guild_id,)
        )
        row = cursor.fetchone()
        return Guilds(**row) if row else None
    

    @ensure_cursor
    def set_guild(
        self,
        gxp: str,
        *,
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            """
                INSERT INTO guilds (guild_id, gxp) 
                VALUES (%s, %s) 
                ON DUPLICATE KEY UPDATE gxp = VALUES(gxp)
            """,
            (self.guild_id, gxp)
        )


    @ensure_cursor
    def remove_guild(self, *, cursor: Cursor = None):
        cursor.execute(
            "DELETE FROM guilds WHERE guild_id=%s", 
            (self.guild_id,)
        )

    
