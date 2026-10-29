###### standard library imports ######
import os
from datetime import datetime, timedelta, date

###### 3rd party imports ######
from dotenv import load_dotenv
import pytz
import requests

###### local imports ######
from apis.models import Game

load_dotenv()


def get_cfb_schedule():
    cfb_api_key = os.getenv("cfb_api_key")
    today = date.today()
    season = today.year - 1 if today.month < 3 else today.year
    headers = {"Authorization": f"Bearer {cfb_api_key}", "accept": "application/json"}

    response = requests.get(
        "https://apinext.collegefootballdata.com/games",
        headers=headers,
        params={"year":season, "team": "Kentucky", "seasonType": "regular"},
    )

    response.raise_for_status()
        
    football_games = response.json()

    games = []
    for raw in football_games:
        game = Game(sport="cfb",
            game_id=raw["id"],
            start=datetime.fromisoformat(raw["startDate"]),
            is_tbd=raw["startTimeTBD"], 
            home=raw["homeTeam"], 
            away=raw["awayTeam"]
        )
        games.append(game)

    return games


def format_cfb_game(game: Game, duration_hours=3.5):
    # converting time zone
    eastern = pytz.timezone("America/New_York")

    # formats date time and time into the right format
    start_dt = game.start.astimezone(eastern)
    
    end_dt = start_dt + timedelta(hours=duration_hours)
    
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    return start_time_formatted, end_time_formatted



if __name__ == "__main__":
    games = get_cfb_schedule()
    print(format_cfb_game(games[0]))
