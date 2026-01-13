from dataclasses import dataclass


@dataclass(slots=True)
class LinkedPlayer:
    discord_id: int
    uuid: str


@dataclass(slots=True)
class Session:
    uuid: str
    session_id: int
    wins: int
    weighted: int
    kills: int
    finals: int
    beds: int
    level: int
    xp: int
    start_time: int