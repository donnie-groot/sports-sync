###### standard libery imports ######
from datetime import datetime, timezone, timedelta

###### 3rd party imports ######

###### local imports ######


###### logic  ######
def create_timed_event(service, summary, start_time_formatted, end_time_formatted):
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


def create_all_day_event(service, summary, game):
    start_date_str = game["startDate"].replace("Z", "")
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S.%f")
    just_the_date = start_dt.date()
    formatted_date = just_the_date.strftime("%Y-%m-%d")
    end_date = just_the_date + timedelta(days=1)
    formatted_end_date = end_date.strftime("%Y-%m-%d")
    event = {
        "summary": summary,
        "start": {"date": formatted_date},
        "end": {"date": formatted_end_date}
    }

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



# grabing all the events
def get_existing_events(service):
    page_token = None

    all_events = []

    while True:
        event_result = (
            service.events().list(calendarId="primary", pageToken=page_token).execute()
        )
        
        events = event_result.get("items", [])

        all_events.extend(events)

        page_token = event_result.get("nextPageToken")
        if not page_token:
            break

    return all_events


def find_match(all_events, game_summary):
    for event in all_events:
        if game_summary == event["summary"]:
            return event
    return None


