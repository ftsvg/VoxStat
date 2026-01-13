from discord import app_commands
from typing import List

MODES: List[app_commands.Choice] = [
    app_commands.Choice(name='Overall', value='Overall'),
    app_commands.Choice(name='Bed Bridge Fight', value='Bed Bridge Fight'), 
    app_commands.Choice(name='Void Fight', value='Void Fight'),
    app_commands.Choice(name='Ground Fight', value='Ground Fight'),
    app_commands.Choice(name='Block Sumo', value='Block Sumo'), 
    app_commands.Choice(name='Beta Block Sumo', value='Beta Block Sumo'), 
    app_commands.Choice(name='Bedwars Normal', value='Bedwars Normal'), 
    app_commands.Choice(name='Sumo Duels', value='Sumo Duels'), 
    app_commands.Choice(name='Stick Fight', value='Stick Fight'), 
    app_commands.Choice(name='Pearl Fight', value='Pearl Fight'), 
    app_commands.Choice(name='Bed Rush', value='Bed Rush'),
    app_commands.Choice(name='Obstacles', value='Obstacles'),
    app_commands.Choice(name='Party Games', value='Party Games'),
    app_commands.Choice(name='Bow Fight', value='Bow Fight'), 
    app_commands.Choice(name='Ladder Fight', value='Ladder Fight'), 
    app_commands.Choice(name='Flat Fight', value='Flat Fight'), 
    app_commands.Choice(name='Resource Collect', value='Resource Collect'), 
    app_commands.Choice(name='Miniwars', value='Miniwars'),
]


MODE_CONFIG: dict[str, dict] = {
    "Overall": {
        "stats": 5,
        "joins": ("overall", None),
        "overall": True,
        "types": {
            "combined": "Overall"
        }
    },
    "Bed Bridge Fight": {
        "stats": 4,
        "joins": ("bridgesSingle", "bridgesDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Void Fight": {
        "stats": 4,
        "joins": ("voidSingle", "voidDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Ground Fight": {
        "stats": 4,
        "joins": ("groundSingle", "groundDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Bedwars Normal": {
        "stats": 4,
        "joins": ("bedwarsNormalSingle", "bedwarsNormalDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Ladder Fight": {
        "stats": 4,
        "joins": ("ladderFightSingle", "ladderFightDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Miniwars": {
        "stats": 4,
        "joins": ("miniwarsSolo", "miniwarsDouble"),
        "types": {"single": "Solo", "double": "Doubles", "combined": "Overall"}
    },
    "Block Sumo": {
        "stats": 2,
        "joins": ("sumo", None),
        "types": {"combined": "Overall"}
    },
    "Beta Block Sumo": {
        "stats": 2,
        "joins": ("betaSumo", None),
        "types": {"combined": "Overall"}
    },
    "Sumo Duels": {
        "stats": 2,
        "joins": ("sumoDuelsSolo", "sumoDuelsDouble"),
        "types": {"single": "Solo", "double": "Doubles", "combined": "Overall"}
    },
    "Stick Fight": {
        "stats": 2,
        "joins": ("stickFightSingle", "stickFightDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Pearl Fight": {
        "stats": 2,
        "joins": ("pearlFightSingle", "pearlFightDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Bed Rush": {
        "stats": 2,
        "joins": ("bedRushSingle", "bedRushDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Bow Fight": {
        "stats": 2,
        "joins": ("bowFightSingle", "bowFightDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Flat Fight": {
        "stats": 2,
        "joins": ("flatFightSingle", "flatFightDouble"),
        "types": {"single": "1v1", "double": "2v2", "combined": "Overall"}
    },
    "Resource Collect": {
        "stats": 2,
        "joins": ("resourceSingle", "resourceDouble"),
        "types": {"single": "Solo", "double": "Doubles", "combined": "Overall"}
    },
    "Obstacles": {
        "stats": 1,
        "joins": ("obstacleSingle", None),
        "types": {"combined": "Overall"}
    },
    "Party Games": {
        "stats": 1,
        "joins": ("partyGames", None),
        "types": {"combined": "Overall"}
    }
}


STAT_LAYOUTS = {
    5: [
        ("Wins", (405, 265), "&f", 16),
        ("Weighted Wins", (645, 265), "&f", 16),
        ("Kills", (365, 345), "&f", 16),
        ("Finals", (525, 345), "&f", 16),
        ("Beds", (685, 345), "&f", 16),

        ("wins",   (405, 290), "&a", 20),
        ("weighted", (645, 290), "&9", 20),
        ("kills",  (365, 370), "&d", 20),
        ("finals", (525, 370), "&c", 20),
        ("beds",   (685, 370), "&e", 20),
    ],
    4: [
        ("Wins", (405, 265), "&f", 16),
        ("Kills", (645, 265), "&f", 16),
        ("Finals", (405, 345), "&f", 16),
        ("Beds", (645, 345), "&f", 16),

        ("wins",   (405, 290), "&a", 20),
        ("beds",   (645, 290), "&e", 20),
        ("kills",  (405, 370), "&9", 20),
        ("finals", (645, 370), "&d", 20),
    ],
    2: [
        ("Wins", (0, 0), "&f", 0),
        ("Kills", (0, 0), "&f", 0),

        ("wins",  (0, 0), "&a", 36),
        ("kills",(0, 0), "&9", 36),
    ],
    1: [
        ("Wins", (0, 0), "&f", 36),
        ("wins", (0, 0), "&a", 36),
    ]
}