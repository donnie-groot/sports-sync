###### standard libery imports ######
import os
import json
from datetime import datetime, timedelta

###### 3rd party imports ######
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# getting google auth working
SCOPES = ["https://www.googleapis.com/auth/calendar"]

###### checking if we have credintals ######


def google_auth():
    creds = None
    # checking if credintals are already saved
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # if they arent getting u loged in
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "sports_api_credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # opening token.json and writing the credintals to it
    with open("token.json", "w") as file:
        file.write(creds.to_json())
    # returning and building a connection to google calendar v3 api
    return build("calendar", "v3", credentials=creds)


# load F1 schedule from local JSON file
with open("f1_schedule_2026.json", "r", encoding="utf-8") as file:
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


# nukeing events because dev is a dumy and ran it 4 times because i thought it didnt work


def nuke(service):
    now = datetime.utcnow().isoformat() + "Z"
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


# main loop
def main():
    service = google_auth()
    nuke(service)
    for race in data["races"]:
        calendar_event(race, service)


# calling main

if __name__ == "__main__":
    main()
