import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_route(start_coords: list, end_coords: list) -> list:
    try:
        api_key = os.getenv("OPEN_ROUTE_KEY")
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        params = {
            'api_key': api_key,
            'start': f"{start_coords[0]}, {start_coords[1]}",
            'end': f"{end_coords[0]}, {end_coords[1]}"
        }
        response = requests.get(f'{url}', params=params)
        data = response.json()
        return data['features'][0]['geometry']["coordinates"]
    except:
        print("Ошибка подлючения open route")
        return []
