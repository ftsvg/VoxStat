from typing import Optional, Iterable

from database import ensure_cursor, Cursor, HistoricalStats



class HistoricalHandler:
    def __init__(self, uuid: str, period: str) -> None:
        self._uuid = uuid
        self._period = period

    @ensure_cursor
    def get_stats(self, *, cursor: Cursor = None) -> Optional[HistoricalStats]:
        cursor.execute(
            """
            SELECT uuid, period, wins, weighted, kills,
                finals, beds, star, xp, last_reset
            FROM historical_stats
            WHERE uuid=%s AND period=%s
            """,
            (self._uuid, self._period),
        )
        row = cursor.fetchone()

        return HistoricalStats(**row) if row else None


    @ensure_cursor
    def get_players(self, *, cursor: Cursor = None) -> Iterable[tuple[str, int]]:
        cursor.execute(
            """
            SELECT uuid, last_reset
            FROM historical_stats
            WHERE period=%s
            """,
            (self._period,),
        )
        return cursor.fetchall()


    @ensure_cursor
    def upsert_stats(
        self,
        wins: int,
        weighted: int,
        kills: int,
        finals: int,
        beds: int,
        star: int,
        xp: int,
        *,
        cursor: Cursor = None,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO historical_stats (
                uuid, period, wins, weighted, kills,
                finals, beds, star, xp, last_reset
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, UNIX_TIMESTAMP())
            ON DUPLICATE KEY UPDATE
                wins=VALUES(wins),
                weighted=VALUES(weighted),
                kills=VALUES(kills),
                finals=VALUES(finals),
                beds=VALUES(beds),
                star=VALUES(star),
                xp=VALUES(xp),
                last_reset=VALUES(last_reset)
            """,
            (
                self._uuid,
                self._period,
                wins,
                weighted,
                kills,
                finals,
                beds,
                star,
                xp,
            )
        )