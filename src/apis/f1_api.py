###### standard library imports ######
import requests
import json
###### 3rd party imports ######
#import from thing i downloaded 

###### local imports ######
# from module import something


def get_f1_schedule():
    response = requests.get("https://api.jolpi.ca/ergast/f1/2026/races.json")
    print(response.status_code)
    print(response.json())
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    get_f1_schedule()
