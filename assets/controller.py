# Python dependencies : pip3.X install request, pyTelegramBotAPI, schedule --> When you add a new dependebcies from pip, restart your IDE to Refresh Changes WTF in 2021
# API used for weather : http://api.weatherapi.com/v1/forecast.json?key=<TOKEN>&q=Lyon&days=0&aqi=yes&alerts=yes 
# API for french region code : https://geo.api.gouv.fr/departements/
# Other ressources  : https://www.atmo-auvergnerhonealpes.fr/un-nouvel-indice-national-de-qualite-de-lair
#                     https://www.atmo-auvergnerhonealpes.fr/article/indices-de-qualite-de-lair

import os 
import sqlite3
from dotenv import load_dotenv

load_dotenv()

URL_WEATHER_API = os.getenv("URL_WEATHER_API")
TOKEN_WEATHER_API= os.getenv("TOKEN_WEATHER_API")
TELEGRAM_BOT_TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")

database_path = os.path.expanduser("~")+"/databases_projects/weathergilant/weathergilant.db" #  /home/$USER/databases_projects/weathergilant/weathergilant.db
dbConnection = sqlite3.connect(database_path,check_same_thread=False)
cursor = dbConnection.cursor()
assetsList = ["pollution","allergies","currentWeather","weatherAlertness"]
