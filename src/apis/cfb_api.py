###### standard library imports ######
import os
from datetime import datetime, timedelta

import pytz
import requests

###### 3rd party imports ######
from dotenv import load_dotenv

###### local imports ######
# from module import something

load_dotenv()


def get_cfb_schedule():
    cfb_api_key = os.getenv("cfb_api_key")

    headers = {"Authorization": f"Bearer {cfb_api_key}", "accept": "application/json"}

    response = requests.get(
        "https://apinext.collegefootballdata.com/games",
        headers=headers,
        params={"year": 2026, "team": "Kentucky", "seasonType": "regular"},
    )

    response.raise_for_status()
    football_games = response.json()

    return football_games


def format_cfb_game(game, duration_hours=3.5):
    # converting time zone
    utc = pytz.utc
    eastern = pytz.timezone("America/New_York")

    # formats date time and time into the right format
    start_time_str = game["startDate"].replace("Z", "")
    start_dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%f")
    start_dt = utc.localize(start_dt).astimezone(eastern)
    end_dt = start_dt + timedelta(hours=duration_hours)
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    return start_time_formatted, end_time_formatted
