###### standard libery imports ######

###### 3rd party imports ######


###### local imports ######

from google_auth import google_auth
from calendar_events import smart_sync
from apis.f1_api import get_f1_schedule, format_f1_session
from apis.cfb_api import format_cfb_game, get_cfb_schedule


# main loop
def main():
    service = google_auth()
    race_weekend = get_f1_schedule()
    #nuke(service)
    for event in race_weekend:
        start, end = format_f1_session(event, f"{event['raceName']} - Race", 2)
        #calendar_event(service, f"{event['raceName']} - Race", start, end)

        start, end = format_f1_session(
            event["Qualifying"], f"{event['raceName']} - Qualifying", 1
        )
        #calendar_event(service, f"{event['raceName']} - Qualifying", start, end)

        if event.get("Sprint"):
            start, end = format_f1_session(
                event["Sprint"], f"{event['raceName']} - Sprint", 1
            )
            #calendar_event(service, f"{event['raceName']} - Sprint", start, end)


# making f1 events 
def build_f1_items(races):
    items = []
    for event in races:
        sessions = [
            (event, "race", 2),
            (event["Qualifying"], "Qualifying", 1)

        ]
        if event.get("Sprint"):
            sessions.append((event["Sprint"], "Sprint", 1))
        
        for session_data, label, duration in sessions:
            summary = f"{event['raceName']} - {label}"

            start, end = format_f1_session(session_data, summary, duration)


            item = {
                "summary": summary,
                "is_tbd": False,
                "start": start,
                "end": end,
            }

            items.append(item)

    return items





# making cfb events
def build_cfb_items(games):
    items = []

    for game in games:
        if game["homeTeam"] == "Kentucky":
            summary = f"Kentucky vs {game['awayTeam']}"

        else:
            summary = f"Kentucky at {game['homeTeam']}"
        
        is_tbd = game["startTimeTBD"]

        if not is_tbd:
            start, end = format_cfb_game(game, summary)
        else:
            start = None
            end = None

        item = {
            "summary": summary,
            "is_tbd": is_tbd,
            "start": start,
            "end": end,
            "game": game,
        }

        items.append(item)
        
    return items











# calling main

if __name__ == "__main__":
    main()
