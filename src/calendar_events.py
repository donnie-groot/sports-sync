###### standard libery imports ######
from datetime import datetime, timezone, timedelta

###### 3rd party imports ######

###### local imports ######


###### logic  ######



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

# finds the matching events 
def find_match(all_events, game_summary):
    for event in all_events:
        if game_summary == event.get("summary", ""):
            return event
    
    return None


# creates the events
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


# makes events for our tbds
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


# deletes events
def delete_event(service, event_id):
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"deleted event {event_id}")
    except Exception as e:
        print(f"FAILED to delete event {event_id}: {e}")


def smart_sync(service, items_to_sync):
    all_events = get_existing_events(service)

    for item in items_to_sync:
        matching_event = find_match(all_events, item["summary"])

        if matching_event is None:
            if not item["is_tbd"]:
                create_timed_event(service, item["summary"], item["start"], item["end"])
            
            else:
                create_all_day_event(service, item["summary"], item["game"])
        
        else:
            if "date" in matching_event["start"] and not item["is_tbd"]:
                delete_event(service, matching_event["id"])
                create_timed_event(service, item["summary"], item["start"], item["end"])