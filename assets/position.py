import requests
from assets.controller import *
from assets.functions import dateFormat

def position(location) :
    
    params = dict(
        key=TOKEN_WEATHER_API,
        q=location,
    )
    
    resp = requests.get(url=URL_WEATHER_API, params=params)
    data = resp.json()
    
    if "location" not in data:
        return "No matching location found."
    else : 

        position=data['location']['name']
        return position