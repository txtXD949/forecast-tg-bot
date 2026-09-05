from collections import namedtuple

import requests

forecast_tuple = namedtuple('FTuple', ('temperature', 'wind_speed', 'wind_direction'))


def deg_to_compass(deg):
    dirs = ['С', 'С-В', 'В', 'Ю-В', 'Ю', 'Ю-З', 'З', 'С-З']
    idx = round(deg / 45) % 8
    return dirs[idx]


def get_forecast(lat, lon):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'current_weather': True
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather = data["current_weather"]
        return forecast_tuple(
            temperature=f'{weather['temperature']}°C',
            wind_speed=f'{int(weather['windspeed'] / 3.6)} м/с',
            wind_direction=f'{deg_to_compass(weather['winddirection'])}'
        )
    else:
        return None
