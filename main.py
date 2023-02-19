import requests
import datetime as dt
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv("C:/Users/Book2/Documents/Env Variables/.env")
SHEET_USER = os.getenv("sheet_user")
SHEET_PASS = os.getenv("sheet_pass")
NIX_APP_ID = os.getenv("nix_app_id")
NIX_API_KEY = os.getenv("nix_api_key")

######   UI   #########
WORKOUT = input("What workout did you complete today? ")

############   GOOGLE SHEETS API   ##################
def update_sheet(exc,dur,cal):
    today = dt.datetime.now()
    date = today.strftime("%m/%d/%Y")
    time = today.strftime("%H:%M:%S")
    basic = HTTPBasicAuth(f'{SHEET_USER}', f'{SHEET_PASS}')
    SHEET_ENDPOINT = "https://api.sheety.co/95f4ef8f4f6b6183d8dcffd957a0383b/bus'sWorkouts/sheet1"
    sheet_header = {
        "Content-Type": "application/json",
        "Authorization": "YnVzX2phY2tzb246bG1ub3AxMjM"
    }

    sheet_parameters = {
        "sheet1": {
            "date": f"{date}",
            "time": f"{time}",
            "exercise": f"{exc}",
            "duration": f"{dur}",
            "calories": f"{cal}"
        }
    }
    content = requests.post(url=SHEET_ENDPOINT,headers=sheet_header,json=sheet_parameters,auth=basic)
    print(content.text)

####    NIX API      ###########
NIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
nix_header = {
    "x-app-id": NIX_APP_ID,
    "x-app-key": NIX_API_KEY,
    "x-remote-user-id": "0",
    "Content-Type": "application/json"
}
nix_parameters = {
    "query": f"{WORKOUT}]",
    "gender": "male",
    "weight_kg": 59.00,
    "height_cm": 170.00,
    "age": 26.00
}
content = requests.post(headers=nix_header, url=NIX_ENDPOINT, json=nix_parameters)
info = content.json()
print(info)
for reps in info["exercises"]:
    excercise = reps["name"]
    duration = reps["duration_min"]
    calories = reps["nf_calories"]
    update_sheet(excercise,duration,calories)


#SHEET URL: https://docs.google.com/spreadsheets/d/1NltLHDhq4bAOUh2KQntzvgeyWlR7DJXpM4uJjnNF-k4/edit#gid=0
