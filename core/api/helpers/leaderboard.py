from typing import Any

from core.api import API, VoxylApiEndpoint, APIError, RateLimitError


class LeaderboardInfo:
    @staticmethod
    async def _safe_request(
        endpoint: VoxylApiEndpoint,
        **params: Any,
    ) -> dict | int:
        try:
            return await API.make_request(endpoint, **params)
        except RateLimitError:
            return 429
        except APIError:
            return 500

    @staticmethod
    async def fetch_leaderboard(
        _type: str,
        num: int = 100,
    ) -> dict | int:
        return await LeaderboardInfo._safe_request(
            VoxylApiEndpoint.LEADERBOARD_NORMAL,
            type=_type,
            num=num,
        )

    @staticmethod
    async def fetch_game_leaderboard(
        ref: str,
        period: str = "weekly",
        _type: str = "wins",
    ) -> dict | int:
        return await LeaderboardInfo._safe_request(
            VoxylApiEndpoint.LEADERBOARD_GAME,
            ref=ref,
            period=period,
            type=_type,
        )