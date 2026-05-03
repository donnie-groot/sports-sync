###### standard libery imports ######
import os
import json
from datetime import datetime, timedelta, timezone

###### 3rd party imports ######
import requests

###### local imports ######

from google_auth import base_dir, google_auth
from calendar_events import calendar_event, nuke
from apis.f1_api import get_f1_schedule


# main loop
def main():
    service = google_auth()
    races = get_f1_schedule()
    nuke(service)
    for race in races:
        calendar_event(race, service)


# calling main

if __name__ == "__main__":
    main()



