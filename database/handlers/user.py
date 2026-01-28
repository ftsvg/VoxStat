from database import ensure_cursor, Cursor, Users


class UserHandler:
    def __init__(self, uuid: str | None = None) -> None:
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


    @ensure_cursor
    def get_all_users(self, *, cursor: Cursor = None) -> list[Users]:
        cursor.execute(
            "SELECT * FROM users"
        )
        rows = cursor.fetchall()

        return [Users(**row) for row in rows] if rows else []
    

    @ensure_cursor
    def update_user(
        self,
        star: int,
        xp: int,
        highest_star: float,
        past_star_weeks: list,
        *,
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            """
                UPDATE users
                SET
                    star = %s,
                    xp = %s,
                    highest_star = %s,
                    past_star_weeks = %s
                WHERE uuid = %s
            """,
            (star, xp, highest_star, past_star_weeks, self.uuid)
        )

    
    @ensure_cursor
    def get_old_guild_members(
        self, 
        guild_id: int, 
        *, 
        cursor: Cursor = None
    ) -> list[str]:
        cursor.execute(
            "SELECT uuid FROM users WHERE guild_id = %s",
            (guild_id,)
        )
        result = cursor.fetchall()
        return [row["uuid"] for row in result]
    

    @ensure_cursor
    def set_guild(
        self, 
        guild_id: int, 
        *, 
        cursor: Cursor=None
    ) -> None:
        cursor.execute("UPDATE users SET guild_id=%s WHERE uuid=%s", (guild_id, self.uuid,))


    @ensure_cursor
    def get_guild_members(
        self,
        guild_id: int,
        *,
        cursor: Cursor = None
    ) -> list[Users]:
        cursor.execute(
            "SELECT * FROM users WHERE guild_id = %s",
            (guild_id,)
        )
        rows = cursor.fetchall()

        return [Users(**row) for row in rows]
    