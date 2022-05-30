import requests
from assets.controller import * 
from assets.functions import *

def currentweather(location) :
    url = URL_WEATHER_API

    params = dict(
        key = TOKEN_WEATHER_API,
        q = location,
        aqi = 'yes',
    )

    resp = requests.get(url=url, params=params)
    data = resp.json() # Check the JSON Response Content documentation below

    if "location" not in data:
        now="No matching location found."
    else :
        now="Location 📍 : "+data['location']['name']+" - "+data['location']['region']+" - "+data['location']['country']+"\n"
        now+="Last update : "+data['current']['last_updated']+"\n\n"
        now+="📈 "+data['current']['condition']['text']+"\n"
        now+="🌡️ Temperature : "+str(data['current']['temp_c'])+"\n"
        now+="         Feelslike : "+str(data['current']['feelslike_c'])+"\n"
        now+="💨 Wind : "+str(data['current']['wind_kph'])+"\n"
        now+="         Direction : "+data['current']['wind_dir']+"\n"
        now+="         Feelslike : "+str(data['current']['feelslike_c'])+"\n"
        now+="         Allergies feeling : "+windAlert(data['current']['wind_kph'])+"\n\n"
        now+="Visibility : "+str(data['current']['vis_km'])+"km - "+visibility((data["current"]["vis_miles"]))+"\n"
        now+="UV index : "+indiceUV((data["current"]["uv"]))+""

    return now