import requests
from assets.controller import *
from assets.functions import dateFormat

def forecastWeather(location,day) :
    
    day = int(day) + 1
    params = dict(
            key=TOKEN_WEATHER_API,
            q=location,
            days=day,
            aqi='yes',
            alert="yes"
        )
    day = int(day) - 1
    resp = requests.get(url=URL_WEATHER_API, params=params)
    data = resp.json()
    
    if "location" not in data:
        return "No matching location found."
    else : 
        if day == 1 or day == 2: # Tomorrow / After tomorrow

            forecastWeather="Location 📍 : "+data['location']['name']+" - "+data['location']['region']+" - "+data['location']['country']+"\n"
            forecastWeather+="Forecast for : "+data['forecast']['forecastday'][day]['date']+"\n\n"
            forecastWeather+="📈 : "+data['forecast']['forecastday'][day]['day']['condition']['text']+"\n\n"
            forecastWeather+="🌡️ Temperature : \n"
            forecastWeather+="           AVG : "+str(data['forecast']['forecastday'][day]['day']['avgtemp_c'])+"\n"
            forecastWeather+="           Max : "+str(data['forecast']['forecastday'][day]['day']['maxtemp_c'])+"\n"
            forecastWeather+="           Min : "+str(data['forecast']['forecastday'][day]['day']['mintemp_c'])+"\n"
            forecastWeather+="💨 Max wind  : "+str(data['forecast']['forecastday'][day]['day']['maxwind_kph'])+"\n"
            forecastWeather+="🌧️ Chance of rain : "+str(data['forecast']['forecastday'][day]['day']['daily_chance_of_rain'])+"%\n"
            forecastWeather+="❄️ Chance of snow : "+str(data['forecast']['forecastday'][day]['day']['daily_chance_of_snow'])+"%\n\n"
            forecastWeather+="🌅 Sunrise : "+data['forecast']['forecastday'][day]['astro']['sunrise']+"\n"
            forecastWeather+="🌇 Sunset : "+data['forecast']['forecastday'][day]['astro']['sunset']+"\n\n"
            forecastWeather+="🌚\n"
            forecastWeather+="     Moonrise : "+data['forecast']['forecastday'][day]['astro']['moonrise']+"\n"
            forecastWeather+="     Moonset : "+data['forecast']['forecastday'][day]['astro']['moonset']+"\n"
            forecastWeather+="     Moon phase : "+data['forecast']['forecastday'][day]['astro']['moon_phase']+"\n"
            forecastWeather+="     Moon illumination : "+str(data['forecast']['forecastday'][day]['astro']['moon_illumination'])+"%\n"
            return forecastWeather

        else : # Today 
            today="Location 📍: "+data['location']['name']+" - "+data['location']['region']+" - "+data['location']['country']+"\n"
            today+="Today : \n\n"
            today+="📈 "+data['current']['condition']['text']+"\n"
            today+="🌡️ Temperature : "+str(data['current']['temp_c'])+"\n"
            today+="         AVG : "+str(data['forecast']['forecastday'][day]['day']['avgtemp_c'])+"\n"
            today+="         Max : "+str(data['forecast']['forecastday'][day]['day']['maxtemp_c'])+"\n"
            today+="         Min : "+str(data['forecast']['forecastday'][day]['day']['mintemp_c'])+"\n"
            today+="💨 Max wind  : "+str(data['forecast']['forecastday'][day]['day']['maxwind_kph'])+"\n"
            today+="🌧️ Chance of rain : "+str(data['forecast']['forecastday'][day]['day']['daily_chance_of_rain'])+"%\n"
            today+="❄️ Chance of snow : "+str(data['forecast']['forecastday'][day]['day']['daily_chance_of_snow'])+"%\n\n"
            today+="🌅 Sunrise : "+data['forecast']['forecastday'][day]['astro']['sunrise']+"\n"
            today+="🌇 Sunset : "+data['forecast']['forecastday'][day]['astro']['sunset']+"\n\n"
            today+="🌚\n"
            today+="     Moonrise : "+data['forecast']['forecastday'][day]['astro']['moonrise']+"\n"
            today+="     Moonset : "+data['forecast']['forecastday'][day]['astro']['moonset']+"\n"
            today+="     Moon phase : "+data['forecast']['forecastday'][day]['astro']['moon_phase']+"\n"
            today+="     Moon illumination : "+str(data['forecast']['forecastday'][day]['astro']['moon_illumination'])+"%\n"

            return today

def weatherAlertness(location) : 

    params = dict(
            key=TOKEN_WEATHER_API,
            q=location,
            aqi='yes',
            alerts="yes"
        )

    resp = requests.get(url=URL_WEATHER_API, params=params)

    data = resp.json() # Check the JSON Response Content documentation below

    if "location" not in data:
        return "No matching location found."
    else : 

        if len(data["alerts"]["alert"]) == 0 : 
            return "No weather forecast alert for this location."
            

        alert = "⚠️ WEATHER ALERT ⚠️\n\n"
        alert += "*Local Weather agency* : "+data['alerts']['alert'][0]['headline']+"\n"
        alert += "*Location*📍 : "+data['location']['name']+" - "+data['location']['country']+"\n\n"
        alert += "*Category* : "+data['alerts']['alert'][0]['category']+"\n"
        alert += "*Event* : "+data['alerts']['alert'][0]['event']+"\n"
        alert += "*Effective* : "+dateFormat(data['alerts']['alert'][0]['effective'])+"\n"
        alert += "*Expires* : "+dateFormat(data['alerts']['alert'][0]['expires'])+"\n"
        alert += "*Description* : \n\n"+data['alerts']['alert'][0]['desc']+""
        
        return alert