from datetime import datetime, timedelta, timezone

from core.api.helpers import PlayerInfo
from database import Session


def calc_projected(
    target_level: int, 
    session: Session, 
    current: PlayerInfo
) -> dict:
    
    stars_gained = current.level - session.star
    if stars_gained <= 0:
        return {"error": "This player must gain at least one star to view projected stats."}  
    
    gained = {
        "wins": current.wins - session.wins,
        "kills": current.kills - session.kills,
        "finals": current.finals - session.finals,
        "beds": current.beds - session.beds,
        "weightedwins": current.weightedwins - session.weighted,
    }

    if all(v <= 0 for v in gained.values()):
        return {"error": "This player needs to gain at least one win/kill to view projected stats."} 

    stars_remaining = target_level - current.level
    if stars_remaining <= 0:
        return {"error": "Target level must be higher than current level."}

    now = datetime.now(timezone.utc) 
    start = datetime.fromtimestamp(session.start_time, tz=timezone.utc)

    elapsed_days = max((now - start).total_seconds() / 86400, 0.01)
    stars_per_day = stars_gained / elapsed_days
    days_to_go = stars_remaining / stars_per_day

    projected_date = now + timedelta(days=days_to_go)

    def scale(stat: str) -> int:
        per_star = gained[stat] / stars_gained
        return int(getattr(current, stat) + per_star * stars_remaining)
    
    return {
        "wins": scale("wins"),
        "kills": scale("kills"),
        "finals": scale("finals"),
        "beds": scale("beds"),
        "weightedwins": scale("weightedwins"),
        "projected_date": projected_date.strftime("%d/%m/%Y"),
    }    
