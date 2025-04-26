# filepath: vscode-copilot-workspace://208f167d-b142-475b-a66c-2a65608ed9c6/little-league-lineup/little-league-lineup/src/constraints.py
{
    "max_players": 9,
    "positions": {
        "infield": {
            "max": 5,
            "required": ["1B", "2B", "3B", "SS", "C"]
        },
        "outfield": {
            "max": 3,
            "required": ["LF", "CF", "RF"]
        },
        "pitcher": {
            "max": 1,
            "required": ["P"]
        }
    },
    "player_constraints": [
        {
            "name": "Player 1",
            "positions": ["1B", "2B"],
            "max_time_infield": 5
        },
        {
            "name": "Player 2",
            "positions": ["3B", "OF"],
            "max_time_outfield": 10
        }
    ]
}