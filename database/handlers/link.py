from typing import Optional

from database import ensure_cursor, Cursor, LinkedPlayer


class LinkHandler:
    def __init__(self, discord_id: int) -> None:
        self._discord_id = discord_id


    @ensure_cursor
    def get_linked_player(self, *, cursor: Cursor = None) -> Optional[LinkedPlayer]:
        cursor.execute(
            "SELECT discord_id, uuid FROM linked WHERE discord_id=%s", (self._discord_id,),
        )
        data = cursor.fetchone()

        return LinkedPlayer(
            discord_id=data[0],
            uuid=data[1]
        ) if data else None
    

    @ensure_cursor
    def link_player(self, uuid: str, *, cursor: Cursor = None) -> None:
        cursor.execute(
            """
            INSERT INTO linked (discord_id, uuid)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE uuid = VALUES(uuid)
            """,
            (self._discord_id, uuid),
        )


    @ensure_cursor
    def unlink_player(self, *, cursor: Cursor = None) -> None:
        cursor.execute(
            "DELETE FROM linked WHERE discord_id=%s", (self._discord_id,)
        )        