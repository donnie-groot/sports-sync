###### standard library imports ######
import os
from datetime import datetime, timedelta, date

###### 3rd party imports ######
from dotenv import load_dotenv
import requests
import pytz

###### local imports ######
from apis.models import Game

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

    response.raise_for_status()

    basketball_games = response.json()

    games = []
    for raw in basketball_games:
        game = Game(sport="cbb",
            game_id=raw["id"],
            start=datetime.fromisoformat(raw["startDate"]),
            is_tbd=raw["startTimeTbd"], 
            home=raw["homeTeam"], 
            away=raw["awayTeam"]
        )
        games.append(game)

    return games


def format_cbb_game(game: Game, duration_hours=2.0):
    # converting time zone
    eastern = pytz.timezone("America/New_York")

    # formats date time and time into the right format
    start_dt = game.start.astimezone(eastern)
    
    end_dt = start_dt + timedelta(hours=duration_hours)
    
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    return start_time_formatted, end_time_formatted



if __name__ == "__main__":
    games = get_cbb_schedule()
    print(format_cbb_game(games[0]))
