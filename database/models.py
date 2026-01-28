from dataclasses import dataclass, field


@dataclass(slots=True)
class Users:
    uuid: str
    discord_id: int | None = None
    guild_id: int | None = None
    star: int | None = None
    xp: int | None = None
    highest_star: float | None = None
    past_star_weeks: list = field(default_factory=list)
    tracklist: bool = False


@dataclass(slots=True)
class Session:
    uuid: str
    session_id: int
    wins: int
    weighted: int
    kills: int
    finals: int
    beds: int
    star: int
    xp: int
    start_time: int


@dataclass(slots=True)
class HistoricalStats:
    uuid: str
    period: str
    wins: int
    weighted: int
    kills: int
    finals: int
    beds: int
    star: int
    xp: int
    last_reset: int


@dataclass(slots=True)
class Charts:
    id: int
    last_xp_chart: int
    last_gxp_chart: int


@dataclass(slots=True)
class Guilds:
    id: int
    guild_id: int
    gxp: int


@dataclass(slots=True)
class Channels:
    id: int
    xp_charts: int
    gxp_charts: int
    applications: int   


@dataclass(slots=True)
class GuildLogsChannel:
    id: int
    guild_id: int
    channel_id: int