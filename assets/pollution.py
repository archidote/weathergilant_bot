import requests
from assets.controller import *
from assets.functions import *

def pollution(location) :

    url = URL_WEATHER_API

    params = dict(
        key = TOKEN_WEATHER_API,
        q = location,
        aqi = 'yes',
    )

    resp = requests.get(url=url, params=params)
    data = resp.json() # Check the JSON Response Content documentation below
    # print (data['location']['name'])*
    if "location" not in data:
        pollution="No matching location found."
    else :
        no2=data["current"]["air_quality"]["no2"]
        pm10=data["current"]["air_quality"]["pm10"]
        o3=data["current"]["air_quality"]["o3"]
        pm2_5=data["current"]["air_quality"]["pm2_5"]
        so2=data["current"]["air_quality"]["so2"]
        
        pollution="Pollution : \n"
        pollution+="Location 📍 : "+data['location']['name']+" - "+data['location']['region']+" - "+data['location']['country']+"\n"
        pollution+="\nno2 : "+pollutionNO2(data["current"]["air_quality"]["no2"])[0]+""
        pollution+="\no3 : "+pollutionO3(data["current"]["air_quality"]["o3"])[0]+""
        pollution+="\npm10 ⚠️ : "+pollutionPM10(data["current"]["air_quality"]["pm10"])[0]+""
        pollution+="\npm 2.5 ⚠️ : "+pollutionPM2_5(data["current"]["air_quality"]["pm2_5"])[0]+""
        pollution+="\nso2 : "+pollutionSO2(data["current"]["air_quality"]["so2"])[0]+""
        pollution+="\n\n*GLOBAL RISK* : "+avgPollution(no2,pm10,o3,pm2_5,so2)+""

    return pollution