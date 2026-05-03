###### standard libery imports ######
import os
import json
from datetime import datetime, timedelta, timezone

###### 3rd party imports ###### 

###### local imports ######
from google_auth import base_dir



# load F1 schedule from local JSON file
with open(os.path.join(base_dir, "..", "data", "f1_schedule_2026.json"), "r", encoding="utf-8") as file:
    data = json.load(file)

###### logic  ######
def calendar_event(races, service):
    # formats date time and lights out time into the right format
    start_time_str = races["date"] + "T" + races["lights_out_time"] + ":00"
    start_dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end_dt = start_dt + timedelta(hours=2)
    start_time_formatted = start_dt.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_formatted = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    # formats our event
    event = {
        "summary": races["name"],
        "start": {"dateTime": start_time_formatted, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time_formatted, "timeZone": "America/New_York"},
    }
    # builds calandar event
    service.events().insert(calendarId="primary", body=event).execute()
    print(f"Added {event['summary']}:")


# TODO add a function that prints the added events like we do in nuke


# nukeing events because dev is a dumy and ran it 4 times because i thought it didnt work


def nuke(service):
    now = datetime.now(timezone.utc).isoformat() + "Z"
    page_token = None
    while True:
        event_result = (
            service.events().list(calendarId="primary", pageToken=page_token).execute()
        )
        events = event_result.get("items", [])
        for event in events:
            if " gp" in event.get("summary", "").lower():
                try:
                    service.events().delete(
                        calendarId="primary", eventId=event["id"]
                    ).execute()
                    print(f"deleted: {event['summary']}")
                except Exception as e:
                    print(f"FAILED to delete {event['summary']}: {e}")
        page_token = event_result.get("nextPageToken")
        if not page_token:
            break

