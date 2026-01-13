from dataclasses import dataclass


@dataclass(slots=True)
class LinkedPlayer:
    discord_id: int
    uuid: str