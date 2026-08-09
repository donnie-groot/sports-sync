###### standard library imports ######
from datetime import datetime, timedelta

##### 3rd party imports ######
import pytz
import requests

###### local imports ######
# from module import something


def get_f1_schedule():
    response = requests.get("https://api.jolpi.ca/ergast/f1/2026/races.json")
    races = response.json()["MRData"]["RaceTable"]["Races"]
    return races


def format_f1_session(session, duration_hours):
    # converting time zone
    utc = pytz.utc
    eastern = pytz.timezone("America/New_York")

    # formats date time and time into the right format
    start_time_str = session["date"] + "T" + session["time"].replace("Z", "")
    start_dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    start_dt = utc.localize(start_dt).astimezone(eastern)
    end_dt = start_dt + timedelta(hours=duration_hours)
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    return start_time_formatted, end_time_formatted
