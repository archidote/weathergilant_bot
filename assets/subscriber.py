from assets.currentWeather import currentweather
from assets.functions import *
from assets.controller import * 

def checkIfUserIsAlreadyASubscriber(tableName,chat_id): 
    
    cursor.execute(f"""SELECT chat_id FROM {tableName} WHERE chat_id={chat_id}""")
    check = cursor.fetchall()
    if len(check) != 0:
        return True 
        # User already exist 
    else :
        # User does not exist 
        return False

def insertSubscriber(chat_id,asset,location) : 

    if asset == "allergies" : 
        try: 
            checkIfFrenchlocationExist(location)

            cursor.execute(f"""INSERT OR IGNORE INTO subscriber_{asset}_alerts(chat_id,location) VALUES ({chat_id},'{location}')""")
            dbConnection.commit()
            return 0
        except: 
            return 1
    else : 

        if currentweather(location) == "No matching location found.": 
            return 1
        else : 
            cursor.execute(f"""INSERT OR IGNORE INTO subscriber_{asset}_alerts(chat_id,location) VALUES ({chat_id},'{location}')""")
            dbConnection.commit()
            return 0

def deleteSubscriber(asset, chat_id) : 

    if checkIfUserIsAlreadyASubscriber("subscriber_"+asset+"_alerts",chat_id) == True : 
        cursor.execute(f"""DELETE FROM subscriber_{asset}_alerts WHERE chat_id = {chat_id}""")
        dbConnection.commit()
        return "You have been unsubsribed from "+asset+" alert !"
    else : 
        return "You can't unbsubsribe if you are not subscribed 😊"

def selectFavoriteAssetFromUser (asset,chat_id) : 

    cursor.execute(f"""SELECT location FROM subscriber_{asset}_alerts WHERE chat_id={chat_id}""")
    location = cursor.fetchall()
    if len(location) != 0 : 
        return location[0][0]
    else : 
        return "You don't have a favorite location for pollution alert"