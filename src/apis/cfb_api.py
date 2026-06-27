###### standard library imports ######
import os 
import json
###### 3rd party imports ######
from dotenv import load_dotenv
import requests
###### local imports ######
# from module import something

load_dotenv()

cfb_api_key = os.getenv("cfb_api_key")

headers = {
    "Authorization": f"Bearer {cfb_api_key}",
    "accept": "application/json"
}

response = requests.get(
    "https://apinext.collegefootballdata.com/games",
    headers=headers,
    params={
        "year": 2026,
        "team": "Kentucky",
        "seasonType": "regular"
    }
)

response.raise_for_status()
games = response.json()

filtered_games = []
for game in games:
    filtered_games.append({
        "season": game["season"],
        "week": game["week"],
        "startDate": game["startDate"],
        "startTimeTBD": game["startTimeTBD"],
        "homeTeam": game["homeTeam"],
        "awayTeam": game["awayTeam"],
        "notes": game["notes"]
    })

with open("data/cfb_games_output.json","w") as file:
    json.dump(filtered_games, file, indent=2)

    __name__ == "__main__"