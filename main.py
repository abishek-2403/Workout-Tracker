import requests
from datetime import datetime
import os

APP_ID = os.environ.get("ENV_APP_ID")
API_KEY = os.environ.get("ENV_API_KEY")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

domain = "https://trackapi.nutritionix.com"
endpoint = "/v2/natural/exercise"
sheet_endpoint = os.environ.get("ENV_SHEET_ENDPOINT")


params = {
    "query": input("What exercises did you do today? ")
}

response = requests.post(url=f"{domain}{endpoint}", json=params, headers=headers)

exercises = response.json()["exercises"]

today = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%H:%M:%S")

sheet_headers = {
    "Authorization": os.environ.get("ENV_AUTH_TOKEN")
}

for i in range(len(exercises)):
    exercise = exercises[i]["name"].title()
    duration = int(exercises[i]["duration_min"])
    calories = int(exercises[i]["nf_calories"])
    input_data = {
        "sheet1": {
            "date": today,
            "time": time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=input_data, headers=sheet_headers)
    print(sheet_response.text)
