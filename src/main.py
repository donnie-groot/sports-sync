###### standard libery imports ######

###### 3rd party imports ######


###### local imports ######

from google_auth import google_auth
from calendar_events import smart_sync
from apis.f1_api import get_f1_schedule, format_f1_session
from apis.cfb_api import format_cfb_game, get_cfb_schedule



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

            start, end = format_f1_session(session_data, duration)


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
            start, end = format_cfb_game(game)
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


# main loop
def main():
    service = google_auth()

    race_weekend = get_f1_schedule()
    f1_items = build_f1_items(race_weekend)
    cfb_games = get_cfb_schedule()
    cfb_items = build_cfb_items(cfb_games)

    items = cfb_items + f1_items

    smart_sync(service, items)


# calling main
if __name__ == "__main__":
    main()
