from database import ensure_cursor, Cursor, Channels, GuildLogsChannel


class ChannelsHandler:
    @ensure_cursor
    def set_channel(
        self, channel_id: int, 
        channel_type: str,
        *,
        cursor: Cursor = None
    ):
        cursor.execute(
            f"""
                UPDATE channels
                SET {channel_type} = %s
                WHERE id = 1
            """,
            (channel_id,)
        )

    @ensure_cursor
    def get_channel(
        self,
        channel_type: str,
        *,
        cursor: Cursor = None
    ) -> int | None:
        
        cursor.execute(
            f"""
                SELECT {channel_type}
                FROM channels
                WHERE id = 1
            """
        )
        row = cursor.fetchone()
        return row[channel_type] if row else None
    

    @ensure_cursor
    def set_guild_logs_channel(
        self,
        guild_id: int,
        channel_id: int,
        *,
        cursor: Cursor = None
    ):
        cursor.execute(
            """
            INSERT INTO guild_logs_channel (guild_id, channel_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                channel_id = VALUES(channel_id)
            """,
            (guild_id, channel_id)
        )


    @ensure_cursor
    def get_guild_logs_channel(
        self,
        guild_id: int,
        *,
        cursor: Cursor = None
    ) -> int | None:
        cursor.execute(
            """
            SELECT channel_id
            FROM guild_logs_channel
            WHERE guild_id = %s
            """,
            (guild_id,)
        )
        row = cursor.fetchone()
        return row["channel_id"] if row else None
    

    @ensure_cursor
    def delete_guild_logs_channel(
        self,
        guild_id: int,
        *,
        cursor: Cursor = None
    ) -> int | None:
        cursor.execute(
            """
            DELETE FROM guild_logs_channel
            WHERE guild_id = %s
            """,
            (guild_id,)
        )
