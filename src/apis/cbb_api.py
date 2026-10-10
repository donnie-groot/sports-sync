###### standard library imports ######
import os
from datetime import datetime, timedelta, date
import json

###### 3rd party imports ######
from dotenv import load_dotenv
import requests

###### local imports ######
# from module import something




load_dotenv()

def get_cbb_schedule():
    cbb_api_key = os.getenv("cbb_api_key")
    today = date.today()
    season = today.year + 1 if today.month >= 8 else today.year

    headers = {"Authorization": f"Bearer {cbb_api_key}", "accept": "application/json"}

    response = requests.get(
        "https://api.collegebasketballdata.com/games",
        headers=headers,
        params={"season":season, "team": "Kentucky",}
    )
    games = response.json()

    filtered = [
        {
            "id": g["id"],
            "season": g["season"],
            "startDate": g["startDate"],
            "startTimeTBD": g["startTimeTbd"],
            "homeTeam": g["homeTeam"],
            "awayTeam": g["awayTeam"],
            "tournament": g["tournament"],
            "neutralSite": g["neutralSite"],
            "notes": g["gameNotes"],
        }
        for g in games
    ]

    with open("data/cbb_games_output.json", "w") as f:
        json.dump(filtered, f, indent=2)


if __name__ == "__main__":
    get_cbb_schedule()