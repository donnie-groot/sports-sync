###### standard libery imports ######
from datetime import timedelta


###### 3rd party imports ######
import pytz
###### local imports ######
from apis.models import Game

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


# creates the events
def create_timed_event(service, summary, start_time_formatted, end_time_formatted, sync_key):
    # formats our event
    event = {
        "summary": summary,
        "start": {"dateTime": start_time_formatted, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time_formatted, "timeZone": "America/New_York"},
        "extendedProperties": {"private": {"sync_key": sync_key}},
    }

    # builds calandar event
    try:
        service.events().insert(calendarId="primary", body=event).execute()
        print(f"Added {event['summary']}:")

    except Exception as e:
        print(f"FAILED to add {event['summary']}: {e}")



# makes events for our tbds
def create_all_day_event(service, summary, game: Game, sync_key):
    eastern = pytz.timezone("America/New_York")

    start_dt = game.start.astimezone(eastern)

    just_the_date = start_dt.date()

    formatted_date = just_the_date.strftime("%Y-%m-%d")

    end_date = just_the_date + timedelta(days=1)

    formatted_end_date = end_date.strftime("%Y-%m-%d")

    event = {
        "summary": summary,
        "start": {"date": formatted_date},
        "end": {"date": formatted_end_date},
        "extendedProperties": {"private": {"sync_key": sync_key}},
    }

    try:
        service.events().insert(calendarId="primary", body=event).execute()
        print(f"Added {event['summary']}:")
    except Exception as e:
        print(f"FAILED to add {event['summary']}: {e}")


# deletes events
def delete_event(service, event_id):
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        print(f"deleted event {event_id}")
    except Exception as e:
        print(f"FAILED to delete event {event_id}: {e}")


#update events
def update_event(service, event_id, summary, start_time_formatted, end_time_formatted, sync_key):
    event = {
        "summary": summary,
        "start": {"dateTime": start_time_formatted, "timeZone": "America/New_York"},
        "end": {"dateTime": end_time_formatted, "timeZone": "America/New_York"},
        "extendedProperties": {"private": {"sync_key": sync_key}},
    }
    
    try:
        service.events().update(
            calendarId="primary",
            eventId=event_id,
            body=event,
        ).execute()
        print(f"Updated {summary}")
    except Exception as e:
        print(f"FAILED to update {summary}: {e}")


def smart_sync(service, items_to_sync):
    all_events = get_existing_events(service)

    events_by_keys = {}
    for event in all_events:
        key = event.get("extendedProperties", {}).get("private", {}).get("sync_key")
        if key:
            events_by_keys[key] = event
    
    for item in items_to_sync:
        matching_event = events_by_keys.get(item["sync_key"])

        if matching_event is None:
            if not item["is_tbd"]:
                create_timed_event(service, item["summary"], item["start"], item["end"], item["sync_key"])

            else:
                create_all_day_event(service, item["summary"], item["game"], item["sync_key"])

        else:
            if "date" in matching_event["start"] and not item["is_tbd"]:
                delete_event(service, matching_event["id"])
                create_timed_event(service, item["summary"], item["start"], item["end"], item["sync_key"])

            elif "dateTime" in matching_event["start"] and not item["is_tbd"]:
                existing_time = matching_event["start"]["dateTime"][:19]
                if existing_time != item["start"]:
                    update_event(service, matching_event["id"], item["summary"], item["start"], item["end"], item["sync_key"])