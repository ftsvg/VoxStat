from database import ensure_cursor, Cursor, Charts


class ChartsHandler:
    @ensure_cursor
    def get_last_send(self, *, cursor: Cursor = None) -> int | None:
        cursor.execute(
            "SELECT * FROM charts WHERE id=%s", (1,)
        )
        row = cursor.fetchone()

        return Charts(**row)
    

    @ensure_cursor
    def update_xp_last_send(
        self,
        unix: int,
        *,
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            "UPDATE charts SET last_xp_chart=%s WHERE id=%s",
            (unix, 1),
        )


    @ensure_cursor
    def update_gxp_last_send(
        self,
        unix: int,
        *,
        cursor: Cursor = None
    ) -> None:
        cursor.execute(
            "UPDATE charts SET last_gxp_chart=%s WHERE id=%s",
            (unix, 1),
        )



