# weathergilant

## How to setup ? 


Add to your ~/.bashrc or ~/.zshrc depending of your shell version the following env variables : 

```
nano .env
```

```
URL_WEATHER_API="https://api.weatherapi.com/v1/forecast.json"
TOKEN_WEATHER_API=""
TELEGRAM_BOT_TOKEN=""
```
Install the required dependencies : 
``` 
python3 -m pip install -r requirements.txt
```
Once the following dependencies has been installed, you can run the bot with the two commands : 

```
python3 index.py &
```