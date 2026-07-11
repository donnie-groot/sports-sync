###### standard libery imports ######

###### 3rd party imports ######


###### local imports ######

from google_auth import google_auth
from calendar_events import calendar_event, nuke
from apis.f1_api import get_f1_schedule, format_f1_session


# main loop
def main():
    service = google_auth()
    race_weekend = get_f1_schedule()
    nuke(service)
    for event in race_weekend:
        start, end = format_f1_session(event, f"{event['raceName']} - Race", 2)
        calendar_event(service, f"{event['raceName']} - Race", start, end)

        start, end = format_f1_session(
            event["Qualifying"], f"{event['raceName']} - Qualifying", 1
        )
        calendar_event(service, f"{event['raceName']} - Qualifying", start, end)

        if event.get("Sprint"):
            start, end = format_f1_session(
                event["Sprint"], f"{event['raceName']} - Sprint", 1
            )
            calendar_event(service, f"{event['raceName']} - Sprint", start, end)


# calling main

if __name__ == "__main__":
    main()
