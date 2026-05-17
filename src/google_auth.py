###### standard libery imports ######
import os

###### 3rd party imports ######
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

###### local imports ######


base_dir = os.path.dirname(os.path.abspath(__file__))

# getting google auth working
SCOPES = ["https://www.googleapis.com/auth/calendar"]

###### checking if we have credintals ######Z


def google_auth():
    creds = None
    # checking if credintals are already saved
    if os.path.exists(os.path.join(base_dir, "..", "config", "token.json")):
        creds = Credentials.from_authorized_user_file(
            os.path.join(base_dir, "..", "config", "token.json"), SCOPES
        )
    # if they arent getting u loged in
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(base_dir, "..", "config", "sports_api_credentials.json"),
            SCOPES,
        )
        creds = flow.run_local_server(port=0)
    # opening token.json and writing the credintals to it
    with open(os.path.join(base_dir, "..", "config", "token.json"), "w") as file:
        file.write(creds.to_json())
    # returning and building a connection to google calendar v3 api
    return build("calendar", "v3", credentials=creds)
