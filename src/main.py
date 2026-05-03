###### standard libery imports ######
import os
import json
from datetime import datetime, timedelta, timezone

###### 3rd party imports ######
import requests

# file imports
from google_auth import base_dir, google_auth
from calendar_events import calendar_event, nuke





# load F1 schedule from local JSON file
with open(os.path.join(base_dir, "..", "data", "f1_schedule_2026.json"), "r", encoding="utf-8") as file:
    data = json.load(file)




# main loop
def main():
    service = google_auth()
    nuke(service)
    for race in data["races"]:
        calendar_event(race, service)


# calling main

if __name__ == "__main__":
    main()
