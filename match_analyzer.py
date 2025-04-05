import requests
from logger import log_signal
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")
API_HOST = "https://api-football-v1.p.rapidapi.com/v3"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def analyze_matches():
    url = f"{API_HOST}/fixtures?live=all"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json().get("response", [])
    signals = []

    for match in data:
        team_home = match['teams']['home']['name']
        team_away = match['teams']['away']['name']
        goals = match['goals']
        elapsed = match['fixture']['status']['elapsed']

        if elapsed <= 45 and goals['home'] + goals['away'] > 0:
            message = f"ГОЛ в первом тайме! {team_home} vs {team_away} — счёт: {goals['home']}:{goals['away']}"
            log_signal(message)
            signals.append(message)

    return signals
