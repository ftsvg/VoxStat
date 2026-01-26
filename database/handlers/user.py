from database import ensure_cursor, Cursor, Users


class UserHandler:
    def __init__(self, uuid: str) -> None:
        self.uuid: str = uuid

    @ensure_cursor
    def get_uuid(self, *, cursor: Cursor = None) -> dict | None:
        cursor.execute(
            "SELECT uuid FROM users WHERE uuid=%s", (self.uuid, )
        )
        data = cursor.fetchone()

        return data[0] if data else None
    

    @ensure_cursor
    def verify_user(self, discord_id: int, *, cursor: Cursor=None) -> None:
        cursor.execute(
            "UPDATE users SET discord_id=%s WHERE uuid=%s", (discord_id, self.uuid)
        )
     
    
    @ensure_cursor
    def insert_new_user(
        self, 
        discord_id: int | None = None,
        guild_id: int | None = None,
        star: int | None = None,
        xp: int | None = None,
        highest_star: float | None = None,
        past_star_weeks: list | None = None,
        tracklist: bool = False,
        *, 
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            """
                INSERT INTO users (
                    uuid, discord_id, guild_id, star, xp, highest_star, past_star_weeks, tracklist
                ) 
                VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
                ) 
            """,
            (self.uuid, discord_id, guild_id, star, xp, highest_star, past_star_weeks, tracklist, )
        )

    
    @ensure_cursor
    def get_user(self, *, cursor: Cursor = None):
        cursor.execute(
            "SELECT * FROM users WHERE uuid=%s",
            (self.uuid,)
        )
        row = cursor.fetchone()

        return Users(**row) if row else None
    

    @ensure_cursor
    def get_user_by_discord_id(self, discord_id: int, *, cursor: Cursor = None):
        cursor.execute(
            "SELECT * FROM users WHERE discord_id=%s",
            (discord_id,)
        )
        row = cursor.fetchone()

        return Users(**row) if row else None    


    @ensure_cursor
    def unverify_user(self, discord_id: int, *, cursor: Cursor = None) -> None:
        cursor.execute(
            "UPDATE users SET discord_id=%s WHERE discord_id=%s", (None, discord_id, )
        )      


    @ensure_cursor
    def delete_user(self, *, cursor: Cursor = None) -> None:
        cursor.execute(
            "DELETE FROM users WHERE uuid=%s", (self.uuid, )
        )

