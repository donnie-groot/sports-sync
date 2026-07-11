###### standard libery imports ######
from datetime import datetime, timezone

###### 3rd party imports ######

###### local imports ######


###### logic  ######
def calendar_event(service, summary, start_time_formatted, end_time_formatted):
    # formats our event
    event = {
        "summary": summary,
        "start": {"dateTime": start_time_formatted, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time_formatted, "timeZone": "America/New_York"},
    }
    # builds calandar event
    try:
        service.events().insert(calendarId="primary", body=event).execute()
        print(f"Added {event['summary']}:")
    except Exception as e:
        print(f"FAILED to add {event['summary}']: {e}}")



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
            if " Grand Prix" in event.get("summary", ""):
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
