###### standard library imports ######
import requests
import json

###### 3rd party imports ######
# import from thing i downloaded

###### local imports ######
# from module import something


def get_f1_schedule():
    response = requests.get("https://api.jolpi.ca/ergast/f1/2026/races.json")
    races = response.json()["MRData"]["RaceTable"]["Races"]
    return races


if __name__ == "__main__":
    get_f1_schedule()


def function_name(params):
     # converting time zone
    utc = pytz.utc
    eastern = pytz.timezone("America/New_York")

    # formats date time and time into the right format
    start_time_str = races["date"] + "T" + races["time"].replace("Z", "")
    start_dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    start_dt = utc.localize(start_dt).astimezone(eastern)
    end_dt = start_dt + timedelta(hours=2)
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")