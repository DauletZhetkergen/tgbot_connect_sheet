import telebot
from telebot import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import datetime


TOKEN = 'YOUR TOKEN'##



#####connect Sheet


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('KEYFILE NAME',scope)##

client = gspread.authorize(creds)

sheet = client.open('Your sheets name').sheet1

#####
bot = telebot.TeleBot(TOKEN)


### HERE STARTS BOT
@bot.message_handler(commands=['start','home'])
def send_welcome(message):
		print(datetime.fromtimestamp(message.date))
		markup = telebot.types.ReplyKeyboardMarkup(row_width=1)########
		beer = telebot.types.KeyboardButton(text='Canned drink - $1')##
		cdrinks = telebot.types.KeyboardButton(text='Beer - $3')#######                    HERE I CREATE A BUTTONS
		special =  telebot.types.KeyboardButton(text='Special - $6')###
		markup.add(beer,cdrinks,special) #######################################
		msg = bot.send_message(message.chat.id,f"Welcome {message.chat.username} to Drink Tab!",reply_markup=markup)
		bot.register_next_step_handler(msg,choose_product)
		


quantity = ""
product = ""
def choose_product(message):
	global product
	if message.text =='Canned drink - $1':
		product = 'Canned drink - $1'
		msg = bot.send_message(message.chat.id,'write Quantity:',reply_markup=keyboardnum())
		bot.register_next_step_handler(msg,quantitys)
	elif message.text == 'Beer - $3':
		product = 'Beer - $3'
		msg = bot.send_message(message.chat.id,'write Quantity:',reply_markup=keyboardnum())
		bot.register_next_step_handler(msg,quantitys)
	elif message.text == 'Special - $6':
		product = 'Special - $6'
		msg = bot.send_message(message.chat.id,'write Quantity:',reply_markup=keyboardnum())
		bot.register_next_step_handler(msg,quantitys)
	else:
		bot.send_message(message.chat.id,'Choose one of them, to restart /home')


def quantitys(message):
	global product,quantity
	quantity = message.text
	bot.send_message(message.chat.id,f"""Your order is: {product} quantity: {quantity}
										Type /home to restart
		""")
	date = datetime.fromtimestamp(message.date)
	username = message.chat.username
	insert_data(username,date,product,quantity)

	zeroo()





def insert_data(username,date,product,quantity):
	try:
		cell = sheet.find(username)
		numberofcol = len(sheet.row_values(cell.row))
		sheet.update_cell(cell.row, numberofcol+1, str(date))
		sheet.update_cell(cell.row, numberofcol+2, product)             ####### HERE I INSERT DATA
		sheet.update_cell(cell.row, numberofcol+3, quantity)
		zeroo()
	except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
		sheet.append_row([username,str(date),product,quantity])
		zeroo()
	
	
def zeroo():
	global product,quantity
	quantity = ""				#######REFRESH ALL VARS
	product = ""
	print(quantity,product)



def keyboardnum():
	markup = types.ReplyKeyboardMarkup(row_width=4)
	beer = types.KeyboardButton(text="1")
	cdrinks = types.KeyboardButton(text="2")
	special =  types.KeyboardButton(text="3")
	markup.add(beer,cdrinks,special) 
	return markup






@bot.message_handler(content_types=["text"])
def balance(message):
	bot.send_message(message.chat.id,"Restart /home")

if __name__ == '__main__':
    bot.polling(none_stop=True)

