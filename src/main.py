###### standard libery imports ######
import logging
import sys
###### 3rd party imports ######

###### local imports ######
from calendar_events import smart_sync
from google_auth import google_auth
from apis.cfb_api import format_cfb_game, get_cfb_schedule
from apis.f1_api import format_f1_session, get_f1_schedule
from apis.models import Game
from apis.cbb_api import format_cbb_game, get_cbb_schedule


logger = logging.getLogger(__name__)

# making f1 events
def build_f1_items(races):
    items = []
    for event in races:
        sessions = [(event, "race", 2), (event["Qualifying"], "Qualifying", 1)]
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
                "sync_key": f"f1-{event['season']}-{event['Circuit']['circuitId']}-{label}",
            }

            items.append(item)

    return items


# making cfb events
def build_cfb_items(games: list[Game]):
    items = []

    for game in games:
        if game.home == "Kentucky":
            summary = f"Kentucky vs {game.away}"

        else:
            summary = f"Kentucky at {game.home}"

        is_tbd = game.is_tbd

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
            "sync_key": f"{game.sport}-{game.game_id}"
        }

        items.append(item)

    return items


#making cbb events
def build_cbb_items(games: list[Game]):
    items = []

    for game in games:
        if game.home == "Kentucky":
            summary = f"Kentucky vs {game.away}"
        else:
            summary = f"Kentucky at {game.home}"
        is_tbd = game.is_tbd
    
        if not is_tbd:
            start, end = format_cbb_game(game)
    
        else:
            start = None
            end = None
    
        item = {
            "summary": summary,
            "is_tbd": is_tbd,
            "start": start,
            "end": end,
            "game": game,
            "sync_key": f"{game.sport}-{game.game_id}"
        }
    
        items.append(item)
    return items

SOURCES = [
    (get_f1_schedule, build_f1_items),
    (get_cfb_schedule, build_cfb_items),
    (get_cbb_schedule, build_cbb_items),
]


# main loop
def main():
    try:
        service = google_auth()
    except Exception:
        logger.exception("FAILED GOOGLE AUTH")
        raise

    failed = False
    
    items = []
    for fetch, build in SOURCES:
        try:
            items.extend(build(fetch()))
        except Exception:
            logger.exception(f"FAILED {fetch.__name__}")
            failed = True

    smart_sync(service, items)

    if failed:
        sys.exit(1)

# calling main
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("sync.log"),
            logging.StreamHandler(),
        ],
    )
    main()
