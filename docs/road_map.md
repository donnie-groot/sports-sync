# v1 minimum viable product - complete ✅

- [x] google auth for google calendar
- [x] f1 schedule as a json
- [x] logic for calendar events to write into google calendar
- [x] nuke function to remove calendar events

# v2 refactor of main and f1 api - complete ✅

- [x] split main into multiple files
- [x] make google_auth a separate file
- [x] add print for adding in a similar way to how we already have deleting events
- [x] add jolpi api for f1
- [x] hook up the api into the rest of the logic
- [x] add logic for sprint races
- [x] add logic for quali

# v3 api and football 🏈 - complete ✅

- [x] implement (https://api.collegefootballdata.com/#/games/GetGames)
- [x] find a solution to make this thing sync because of football
- [x] add token refresh to apis
- [x] add error handling to apis
- [x] add smart sync
- [x] add requirements.txt

# v4 basketball 🏀 - work in progress 🔨

- [x] implement https://api.collegebasketballdata.com/
- [x] swap summary for ids (sync keys)
- [x] Game dataclass for normalized game data
- [x] SOURCES list in main so a new sport is one line
- [x] per sport error handling so if one api has an issue it doesn't kill the run
- [x] f1: use `current` season instead of hardcoded 2026
- [ ] swap print statements for logging (in progress)
- [ ] let api errors bubble up to main instead of double reporting
- [ ] fail the run (red in Actions) if any sport or calendar call failed
- [ ] run summary line (synced / added / updated / failed)
- [ ] make a config.toml for team, timezone (per sport calendars later)

# v4.1 public repo polish

- [ ] README (what it does, screenshot, how it runs, design)
- [ ] pyproject: real description, only direct dependencies
- [ ] switch Actions to uv, delete both requirements.txt files
- [ ] keepalive so GitHub doesn't disable the schedule after 60 days
- [x] delete stray src/apis/venv folder

# v4.5 refactor

- [x] matching by summary string → sync keys
- [x] fragile .%f datetime parsing → fromisoformat
- [ ] move summary, sync_key, duration onto Game
- [ ] neutral site support ("vs" instead of "at")
- [ ] sync: update TBD games whose date moved (flex games)
- [ ] sync: push summary changes to existing events
- [ ] sync: delete events for games removed from the schedule (only for sports that fetched successfully!)
- [ ] batch Google Calendar writes (~1s per event right now, profiled with Tachyon)
- [ ] only fetch our own events (source tag + privateExtendedProperty) to cut the ~4s baseline
- [ ] per sport calendars
- [ ] pytz → zoneinfo
- [ ] google_auth cleanup (imports, path handling, creds.valid check)
- [ ] fix typos in comments
- [ ] add type hints
- [ ] add docstrings
- [ ] unit tests with pytest (rename `api tests` folder, pytest pythonpath)

# v5 wwe 🤼 - planned

- [ ] see if there's an api that covers wwe events
- [ ] maybe https://www.thesportsdb.com/league/4444-wwe, or scrape Wikipedia PLE infoboxes
- [ ] general Event class (or named-event class) so F1 and WWE share a shape

# v6 cs2 🔫 - concept of a plan 🤔

- [ ] decide scope (majors only / big tournaments / tournament spans + playoffs)
- [ ] add (https://developers.pandascore.co/docs/websockets-overview) api

# v7 front end