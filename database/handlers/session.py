from typing import Optional, List

from database import ensure_cursor, async_ensure_cursor, Cursor, Session
from core.api.helpers import PlayerInfo


class SessionHandler:
    def __init__(self, uuid: str, session_id: int) -> None:
        self._uuid = uuid
        self._session_id = session_id


    @ensure_cursor
    def get_session(self, *, cursor: Cursor = None) -> Optional[Session]:
        cursor.execute(
            """
            SELECT uuid, session_id, wins, weighted, kills,
                   finals, beds, star, xp, start_time
            FROM sessions
            WHERE uuid=%s AND session_id=%s
            """,
            (self._uuid, self._session_id),
        )
        data = cursor.fetchone()

        return Session(**data) if data else None


    @ensure_cursor
    def get_active_sessions(self, *, cursor: Cursor = None) -> List[int]:
        cursor.execute(
            "SELECT session_id FROM sessions WHERE uuid=%s",
            (self._uuid,),
        )
        rows = cursor.fetchall()
        
        return [row[0] for row in rows] if rows else []


    @async_ensure_cursor
    async def create_session(self, *, cursor: Cursor = None) -> None:
        player = await PlayerInfo.fetch(self._uuid)

        cursor.execute(
            """
            INSERT INTO sessions (
                uuid, session_id, wins, weighted, kills,
                finals, beds, star, xp, start_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
                wins=VALUES(wins),
                weighted=VALUES(weighted),
                kills=VALUES(kills),
                finals=VALUES(finals),
                beds=VALUES(beds),
                star=VALUES(star),
                xp=VALUES(xp),
                start_time=VALUES(start_time)
            """,
            (
                self._uuid,
                self._session_id,
                player.wins,
                player.weightedwins,
                player.kills,
                player.finals,
                player.beds,
                player.level,
                player.exp,
            )
        )

    @async_ensure_cursor
    async def reset_session(self, *, cursor: Cursor = None) -> None:
        player = await PlayerInfo.fetch(self._uuid)

        cursor.execute(
            """
            UPDATE sessions
            SET wins=%s,
                weighted=%s,
                kills=%s,
                finals=%s,
                beds=%s,
                star=%s,
                xp=%s,
                start_time=UNIX_TIMESTAMP()
            WHERE uuid=%s AND session_id=%s
            """,
            (
                player.wins,
                player.weightedwins,
                player.kills,
                player.finals,
                player.beds,
                player.level,
                player.exp,
                self._uuid,
                self._session_id,
            )
        )


    @ensure_cursor
    def end_session(self, *, cursor: Cursor = None) -> None:
        cursor.execute(
            "DELETE FROM sessions WHERE uuid=%s AND session_id=%s",
            (self._uuid, self._session_id),
        )