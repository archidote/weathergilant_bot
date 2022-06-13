import telebot
import schedule 
import time as t 
from telebot import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from assets.functions import *
from assets.controller import *
from assets.currentWeather import currentweather 
from assets.forecastWeather import *
from assets.position import position
from assets.pollution import pollution
from assets.allergies import allergies
from assets.subscriber import *

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

############################################# LOGS stderr ############################################

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger()

# fileHandler = logging.FileHandler("{0}/{1}.txt".format("others/logs/", "logs"))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

#consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

############################################# LOGS stderr ############################################

@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	bot.reply_to(message, "Hello "+message.from_user.first_name+" 👋 !! Welcome to weathergilant bot. tap /help to know supported command :) ", reply_markup=markup)
 
############################################# LOCATION specific Menu - Start ############################################

@bot.message_handler(commands=['location'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location_button = types.KeyboardButton(text='Share your position📍', request_location=True)
    markup.add(location_button)
    bot.reply_to(message, "Share your location to get your weather's town", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def got_location(message):
	markup = InlineKeyboardMarkup()
	geoCoordinates = str(message.location.latitude)+","+str(message.location.longitude)
	location = position(geoCoordinates)
	global rootLocation 
	rootLocation = location		
	b1 = InlineKeyboardButton(text='Today', callback_data = 'today_location')
	b2 = InlineKeyboardButton(text='Tomorrow', callback_data = 'tomorrow_location')
	b3 = InlineKeyboardButton(text='After tomorrow', callback_data = 'after_tomorrow_location')
	b4 = InlineKeyboardButton(text='Weather alertness ?', callback_data = 'weatherAlertness_location')
	b5 = InlineKeyboardButton(text='Pollution', callback_data = 'pollution_location')
	markup.add(b1, b2, b3, b4, b5)
	bot.reply_to(message,location,reply_markup=markup)
 
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'others/audio/{message.chat.id}_{int(time())}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
 
############################################# LOCATION specific Menu - END ############################################

############################################# Main Menu - Start ############################################

@bot.message_handler(commands=['weather'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a town to get weather information :", reply_markup=markup)

@bot.message_handler(commands=['weather_alertness'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a town to know if a weather alert is happening now :", reply_markup=markup)

@bot.message_handler(commands=['pollution'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a town to get the pollution information :", reply_markup=markup)

@bot.message_handler(commands=['allergies_fr'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup = telebot.types.ForceReply()
	bot.reply_to(message, "Enter a french region code location to get the allergies report (EX : 69) :", reply_markup=markup)
 
@bot.message_handler(commands=['subscribe'])
def send_welcome(message):
	markup = InlineKeyboardMarkup()	
	b1 = InlineKeyboardButton(text='Current Weather', callback_data = 'subscribe_currentWeather_alerts')
	b2 = InlineKeyboardButton(text='Weather alertness', callback_data = 'subscribe_weatherAlertness_alerts')
	b3 = InlineKeyboardButton(text='Pollution', callback_data = 'subscribe_pollution_alerts')
	b4 = InlineKeyboardButton(text='Allergies', callback_data = 'subscribe_allergies_alerts')
	b5 = InlineKeyboardButton(text='unsubscribe_all', callback_data = 'unsubscribe_all')
	markup.add(b1, b2, b3, b4, b5)
	bot.reply_to(message, "Subscribe Menu :", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):

	helpMenu = """ℹ️ *Help Menu* ℹ️\n
	/weather Show weather forecast. ex : Paris \n
	/location - Show weather information and more for your current location\n
	/pollution - Show live pollution indexes. ex : Paris \n
	/allergies\_fr - Show allergies for a french departement. ex : 69\n
	/weather\_alertness - Show if a weather alertness is currently underway. ex : London\n
	/subscribe - Menu to subscribe to custom alert(s)"""

	bot.reply_to(message,helpMenu,parse_mode="markdown")
 
def sendMessageAuto(asset):

	print ("hello")
	dic = { # Dictionnary of functions who for create a dynamic affectation below
	"pollution": pollution,
	"allergies":allergies,
	"weatherAlertness":weatherAlertness,
	"currentWeather":currentweather
	}

	cursor.execute(f"""SELECT * FROM subscriber_{asset}_alerts""")

	rows = cursor.fetchall()

	markup="""{"inline_keyboard":[[{"text":"Unsubscribe","callback_data":"unsubscribe_"""+asset+"""_alerts"}],[{"text":"🔄 Refresh","callback_data":"refresh_"""+asset+"""_request_from_alert"}]]}"""

	for row in rows:

		bot_chatID = str(row[0]) # chat_id stored into the table subscriber_allergies_alerts

		dynamicFunction = dic[asset]
		bot_message = dynamicFunction(row[1])
  
		print (bot_chatID)
		print (bot_message)
  
		bot.send_message(bot_chatID,bot_message,disable_web_page_preview=True,reply_markup=markup)

 
 ############################################# Main Menu - End ############################################
 
 ############################################# reply_to_message Menu - Start ############################################

@bot.message_handler(func=lambda m: True)
def which_reply(message):
	if message.reply_to_message == None : 
		bot.reply_to(message, "*Command not found* \nTap /help to get all of the available command",parse_mode="MarkdownV2")
	else :
		if message.reply_to_message.text == "Enter a town to get weather information :" : # Warning, here the sentence must be the same that the previous one for the answser context !!!
			markup = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Today', callback_data = 'today')
			b2 = InlineKeyboardButton(text='Tomorrow', callback_data = 'tomorrow')
			b3 = InlineKeyboardButton(text='After tomorrow', callback_data = 'after_tomorrow')
			markup.add(b1, b2, b3)
			bot.reply_to(message, currentweather(message.text), reply_markup=markup)

		elif message.reply_to_message.text == "Enter a town to know if a weather alert is happening now :" :
			if weatherAlertness(message.text) == "No matching location found." :
				bot.reply_to(message, "No matching location found.")
			elif weatherAlertness(message.text) == "No weather forecast alert for this location.\n" :
				bot.reply_to(message, "No weather forecast alert for this location.\n")
			else : 
				inline = InlineKeyboardMarkup()
				refreshButton = InlineKeyboardButton(text='🔄 Refresh', callback_data = 'refresh_weatherAlerness_request')
				inline.add(refreshButton)
				bot.reply_to(message, weatherAlertness(message.text),reply_markup=inline) 

		elif message.reply_to_message.text == "Enter a town to get the pollution information :" :
			if pollution(message.text) == "No matching location found." :
				bot.reply_to(message, "No matching location found.")
			else : 
				inline = InlineKeyboardMarkup()
				refreshButton = InlineKeyboardButton(text='🔄 Refresh', callback_data = 'refresh_pollution_request')
				inline.add(refreshButton)
				bot.reply_to(message, pollution(message.text),reply_markup=inline) 

		elif message.reply_to_message.text == "Enter a french region code location to get the allergies report (EX : 69) :" :
			if allergies(message.text) == "Wrong location code (FR) !" :
				bot.reply_to(message, "Wrong location code (FR) !")
			else : 
				inline = InlineKeyboardMarkup()
				refreshButton = InlineKeyboardButton(text='🔄 Refresh', callback_data = 'refresh_allergies_request')
				inline.add(refreshButton)
				bot.reply_to(message, allergies(message.text),reply_markup=inline) 

		elif message.reply_to_message.text == "Enter your region code to be notifyed about allergies. (Work only for FR) Ex : 69" :
    			
			if insertSubscriber(str(message.chat.id),"allergies",message.text) == 1 :
				bot.reply_to(message,"Wrong location code (FR) ! ")
			else :
				bot.reply_to(message,"You are now registered for allergies alert 😊")

		elif message.reply_to_message.text == "Enter your location name to be notifyed every day of pollution. Ex : Paris" :
			if insertSubscriber(str(message.chat.id),"pollution",message.text) == 1 :
				bot.reply_to(message,"No matching location found.")
			else : 
				bot.reply_to(message,"You are now registered for pollution alert 😊")

		elif message.reply_to_message.text == "Enter your location name to be notifyed every day of current weather. Ex : Paris" :
			if insertSubscriber(str(message.chat.id),"currentWeather",message.text) == 1 :
				bot.reply_to(message,"No matching location found.")
			else : 
				bot.reply_to(message,"You are now registered for current weather alert 😊")

		elif message.reply_to_message.text == "Enter your location name to be notifyed every day if a weather alertness occur. Ex : Paris" :
			if insertSubscriber(str(message.chat.id),"weatherAlertness",message.text) == 1 :
				bot.reply_to(message,"No matching location found.")
			else : 
				bot.reply_to(message,"You are now registered for weather alertness alert 😊")

 ############################################# reply_to_message Menu - End ############################################
 
 ############################################# Call back zone - Start ############################################

@bot.callback_query_handler(func=lambda call: call.data != 'check_group') # Buttons fetch reply value 
def callback_inline(call):

	if call.data == "today":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(call.message.reply_to_message.text,0), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of today for : "+call.message.reply_to_message.text)

	if call.data == "tomorrow":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(call.message.reply_to_message.text,1), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of tomorrow for : "+call.message.reply_to_message.text)

	if call.data == "after_tomorrow":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(call.message.reply_to_message.text,2), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of after tomorrow for : "+call.message.reply_to_message.text)
  
	if call.data == "today_location":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(rootLocation,0), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of today for :"+rootLocation)
  
	if call.data == "tomorrow_location":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(rootLocation,1), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of tomorrow for : "+rootLocation)
  
	if call.data == "after_tomorrow_location":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=forecastWeather(rootLocation,2), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying weather of tomorrow for : "+rootLocation)
  
	if call.data == "pollution_location":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=pollution(rootLocation), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Displaying pollutiion index for : "+rootLocation)
  
	if call.data == "weatherAlertness_location":
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=weatherAlertness(rootLocation), reply_markup=call.message.reply_markup)
		bot.answer_callback_query(call.id, "Weather alertness ?  : "+rootLocation)
  
	
	if call.data == "refresh_pollution_request":
		originalMessage = len(call.message.text)
		refreshMessage = len(pollution(call.message.reply_to_message.text))
		if originalMessage == refreshMessage : 
			bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
		else : 
			bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=pollution(call.message.reply_to_message.text), reply_markup=call.message.reply_markup)
			bot.answer_callback_query(call.id, "Data updated")
   
   
	if call.data == "subscribe_currentWeather_alerts":
		check = checkIfUserIsAlreadyASubscriber("subscriber_currentWeather_alerts",str(call.message.chat.id))
		if check == True :
			location = selectFavoriteAssetFromUser("currentWeather",str(call.message.chat.id))
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			inline = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_currentWeather_alerts')
			inline.add(b1)
			bot.reply_to(call.message,"You are already subscribed (location : <b>"+location+"</b>) !\nIf you want to unsubscribe, click on the button below.", reply_markup=inline,parse_mode="html")
		else : 
			markup = telebot.types.ForceReply()
			bot.reply_to(call.message, "Enter your location name to be notifyed every day of current weather. Ex : Paris", reply_markup=markup, parse_mode="markdown")

	if call.data == "subscribe_weatherAlertness_alerts":
		check = checkIfUserIsAlreadyASubscriber("subscriber_weatherAlertness_alerts",str(call.message.chat.id))
		if check == True :
			location = selectFavoriteAssetFromUser("weatherAlertness",str(call.message.chat.id))
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			inline = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_weatherAlertness_alerts')
			inline.add(b1)
			bot.reply_to(call.message,"You are already subscribed (location : <b>"+location+"</b>) !\nIf you want to unsubscribe, click on the button below.", reply_markup=inline,parse_mode="html")
		else : 
			markup = telebot.types.ForceReply()
			bot.reply_to(call.message, "Enter your location name to be notifyed every day if a weather alertness occur. Ex : Paris", reply_markup=markup, parse_mode="markdown")
   
	if call.data == "subscribe_pollution_alerts":
		check = checkIfUserIsAlreadyASubscriber("subscriber_pollution_alerts",str(call.message.chat.id))
		if check == True :
			location = selectFavoriteAssetFromUser("pollution",str(call.message.chat.id))
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			inline = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_pollution_alerts')
			inline.add(b1)
			bot.reply_to(call.message,"You are already subscribed (location : <b>"+location+"</b>) !\nIf you want to unsubscribe, click on the button below.", reply_markup=inline,parse_mode="html")
		else : 
			markup = telebot.types.ForceReply()
			bot.reply_to(call.message, "Enter your location name to be notifyed every day of pollution. Ex : Paris", reply_markup=markup, parse_mode="markdown")
   
	if call.data == "subscribe_allergies_alerts":
		check = checkIfUserIsAlreadyASubscriber("subscriber_allergies_alerts",str(call.message.chat.id))
		if check == True :
			location = selectFavoriteAssetFromUser("allergies",str(call.message.chat.id))
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			inline = InlineKeyboardMarkup()
			b1 = InlineKeyboardButton(text='Unsubscribe', callback_data = 'unsubscribe_allergies_alerts')
			inline.add(b1)
			bot.reply_to(call.message,"You are already subscribed (location : <b>"+location+"</b>) !\nIf you want to unsubscribe, click on the button below.", reply_markup=inline,parse_mode="html")
		else : 
			markup = telebot.types.ForceReply()
			bot.reply_to(call.message, "Enter your region code to be notifyed about allergies. (Work only for FR) Ex : 69", reply_markup=markup, parse_mode="markdown")
   
	if call.data == "unsubscribe_all":
		j = 0 
		for asset in assetsList :
			check = checkIfUserIsAlreadyASubscriber("subscriber_"+asset+"_alerts",str(call.message.chat.id))
			j = j + 1 
			if check == True :
				location = selectFavoriteAssetFromUser(asset,str(call.message.chat.id))
				bot.reply_to(call.message, deleteSubscriber(asset,call.message.chat.id), parse_mode="markdown")
		bot.reply_to(call.message, "Unsubscribed from all alerts.",parse_mode="markdown")

   
	if call.data == "refresh_allergies_request":
		originalMessage = len(call.message.text)
		refreshMessage = len(allergies(call.message.reply_to_message.text))
		if originalMessage == refreshMessage : 
			bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
		else : 
			bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=allergies(call.message.reply_to_message.text), reply_markup=call.message.reply_markup)
			bot.answer_callback_query(call.id, "Data updated")

	if call.data == "refresh_weatherAlerness_request":
		originalMessage = len(call.message.text)
		refreshMessage = len(weatherAlertness(call.message.reply_to_message.text))
		if originalMessage == refreshMessage : 
			bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
		else : 
			bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=weatherAlertness(call.message.reply_to_message.text), reply_markup=call.message.reply_markup)
			bot.answer_callback_query(call.id, "Data updated")

	if call.data == "refresh_allergies_request_from_alert":
		alertRefresh=selectFavoriteAssetFromUser("allergies",call.message.chat.id)
		originalMessage = len(call.message.text)
		refreshMessage = len(allergies(alertRefresh))		
		if alertRefresh != 0 : 
			if originalMessage == refreshMessage : 
				bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
			else : 
				bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=allergies(alertRefresh), reply_markup=call.message.reply_markup)
				bot.answer_callback_query(call.id, "Data updated")
    
	if call.data == "refresh_weatherAlertness_request_from_alert":
		alertRefresh=selectFavoriteAssetFromUser("weatherAlertness",call.message.chat.id)
		originalMessage = len(call.message.text)
		refreshMessage = len(weatherAlertness(alertRefresh))	
		if alertRefresh != 0 : 
			if originalMessage == refreshMessage : 
				bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
			else : 
				bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=weatherAlertness(alertRefresh), reply_markup=call.message.reply_markup)
				bot.answer_callback_query(call.id, "Data updated")

	if call.data == "refresh_currentWeather_request_from_alert":
		alertRefresh=selectFavoriteAssetFromUser("currentWeather",call.message.chat.id)
		originalMessage = len(call.message.text)
		refreshMessage = len(currentweather(alertRefresh))	
		if alertRefresh != 0 : 
			if originalMessage == refreshMessage : 
				bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
			else : 
				bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=currentweather(alertRefresh), reply_markup=call.message.reply_markup)
				bot.answer_callback_query(call.id, "Data updated")
    
	if call.data == "refresh_pollution_request_from_alert":
		alertRefresh=selectFavoriteAssetFromUser("pollution",call.message.chat.id)
		originalMessage = len(call.message.text)
		refreshMessage = pollution(alertRefresh)
		if alertRefresh != 0 : 
			originalMessage = len(call.message.text)
			refreshMessage = len(pollution(alertRefresh))
			# print(repr(originalMessage)) print raw data of this variable, to demystified it
			if originalMessage == refreshMessage : # 
				bot.answer_callback_query(call.id, "Data has not been updated since your previous request")
			else : 
				bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=pollution(alertRefresh), reply_markup=call.message.reply_markup)
				bot.answer_callback_query(call.id, "Data updated")


 ############################################# Subscriber call back area Menu - Start ############################################
	
	if call.data == "cancel":
		bot.delete_message(call.message.chat.id, call.message.message_id)

	if call.data == "unsubscribe_allergies_alerts":
		markup = InlineKeyboardMarkup()
		b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_allergies_alerts_confirm')
		b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
		markup.add(b1, b2)
		bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>allergie</b> alerts?", reply_markup=markup, parse_mode="html")
		bot.answer_callback_query(call.id, "Are you sure?")

	if call.data == "unsubscribe_pollution_alerts":
		markup = InlineKeyboardMarkup()
		b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_pollution_alerts_confirm')
		b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
		markup.add(b1, b2)
		bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>pollution</b> alerts?", reply_markup=markup, parse_mode="html")
		bot.answer_callback_query(call.id, "Are you sure?")

	if call.data == "unsubscribe_currentWeather_alerts":
		markup = InlineKeyboardMarkup()
		b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_currentWeather_alerts_confirm')
		b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
		markup.add(b1, b2)
		bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>current weather</b> alerts?", reply_markup=markup, parse_mode="html")
		bot.answer_callback_query(call.id, "Are you sure?")

	if call.data == "unsubscribe_weatherAlertness_alerts":
		markup = InlineKeyboardMarkup()
		b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_weatherAlertness_alerts_confirm')
		b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
		markup.add(b1, b2)
		bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>weather alertness</b> alerts?", reply_markup=markup, parse_mode="html")
		bot.answer_callback_query(call.id, "Are you sure?")
  
	# if call.data == "unsubscribe_all":
	# 	markup = InlineKeyboardMarkup()
	# 	b1 = InlineKeyboardButton(text='Yes', callback_data = 'unsubscribe_weatherAlertness_alerts_confirm')
	# 	b2 = InlineKeyboardButton(text='No', callback_data = 'cancel')
	# 	markup.add(b1, b2)
	# 	bot.send_message(call.message.chat.id, text="Are you sure you want <b>unsubscribe</b> to <b>weather alertness</b> alerts?", reply_markup=markup, parse_mode="html")
	# 	bot.answer_callback_query(call.id, "Are you sure?")

	if call.data == "unsubscribe_allergies_alerts_confirm":
		bot.answer_callback_query(call.id, "You unsubscribed to allergie alerts")
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("allergies",call.message.chat.id))

	if call.data == "unsubscribe_pollution_alerts_confirm":
		bot.answer_callback_query(call.id, "You unsubscribed to pollution alerts")
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("pollution",call.message.chat.id))

	if call.data == "unsubscribe_currentWeather_alerts_confirm":
		bot.answer_callback_query(call.id, "You unsubscribed to current weather alerts")
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("currentWeather",call.message.chat.id))

	if call.data == "unsubscribe_weatherAlertness_alerts_confirm":
		bot.answer_callback_query(call.id, "You unsubscribed to weather alertness alerts")
		bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("weatherAlertness",call.message.chat.id))
  
	# if call.data == "unsubscribe_all_confirm":
	# 	bot.answer_callback_query(call.id, "You unsubscribed to weather alertness alerts")
	# 	bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=deleteSubscriber("weatherAlertness",call.message.chat.id))
  
 ############################################# Subscriber area Menu - End ############################################
 
###################################################################################################################
#                                                SEND CUSTOMS ALERTS                                              #
###################################################################################################################  

schedule.every().day.at("07:00").do(lambda: sendMessageAuto("weatherAlertness"))
schedule.every().day.at("07:00").do(lambda: sendMessageAuto("currentWeather"))
schedule.every().day.at("07:00").do(lambda: sendMessageAuto("pollution"))
schedule.every().day.at("07:00").do(lambda: sendMessageAuto("allergies"))


def schedule_send_message_auto(): 
    while True:
        schedule.run_pending()
        t.sleep(1)

t1 = threading.Thread(target = schedule_send_message_auto)
t1.start()

bot.infinity_polling() # Bot Execution
