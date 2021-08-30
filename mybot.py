import const
import telebot
from telebot import types
from geopy.distance import geodesic


bot = telebot.TeleBot(const.API_TOKEN)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_address = types.KeyboardButton('Адреса магазинов', request_location= True)
btn_payment = types.KeyboardButton('Способы оплаты')
btn_delivery = types.KeyboardButton('Способы доставки')
btn_time_work = types.KeyboardButton('Время работы')
markup_menu.add(btn_address, btn_delivery, btn_payment,btn_time_work)

markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные',callback_data='cash')
btn_in_card = types.InlineKeyboardButton('Картой',callback_data='card')
btn_in_invoice = types.InlineKeyboardButton('Перевод',callback_data='invose')

markup_inline_payment.add(btn_in_cash, btn_in_card, btn_in_invoice)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Я бот интернет магазина!\n Что Вас интересует?\n Вы можете ознакомиться со следующей информацией: \n адрес, способ оплаты и способ доставки,время работы \n для этого нажмите выбранную кнопку ниже. ", reply_markup=markup_menu )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if message.text == 'Способы доставки':
		bot.reply_to(message, 'Доставка курьером, самовывоз, почта России', reply_markup=markup_menu)
	elif message.text == 'Способы оплаты':
		bot.reply_to(message, 'В наших магазинах доступны следующие способы оплаты ', reply_markup=markup_inline_payment)
	elif message.text == 'Время работы':
		bot.reply_to(message, 'Наши магазины работают с 9 до 18, с понедельника по пятницу ', reply_markup=markup_menu)
	else:
		bot.reply_to(message, message.text,reply_markup=markup_menu)

@bot.message_handler(func=lambda message: True, content_types=['location'])
def magazin_location(message):
	lon = message.location.longitude
	lat = message.location.latitude

	distance = []
	for m in const.MAGAZINS:
		result = geodesic((m['latm'], m['lonm']),(lat, lon)).kilometers
		distance.append(result)
	index = distance.index(min(distance))
	km = min(distance)


	bot.send_message(message.chat.id,'Ближайший к Вам машазин находиться '+ str(round(km))+ ' км от Вас ' )
	bot.send_venue(message.chat.id,
				   const.MAGAZINS[index]['latm'],
				   const.MAGAZINS[index]['lonm'],
				   const.MAGAZINS[index]['title'],
				   const.MAGAZINS[index]['adress'])

@bot.callback_query_handler(func=lambda call:True)
def call_back_payment(call):
	if call.data == 'cash':
		bot.send_message(call.message.chat.id, text='Наличная оплата производиться в рублях в кассах магазинах',reply_markup=markup_inline_payment)
	if call.data == 'card':
		bot.send_message(call.message.chat.id, text='Оплата через терминал',reply_markup=markup_inline_payment)
	if call.data == 'invose':
		bot.send_message(call.message.chat.id, text='Перевод нужно сделать на Карту сбербанка',reply_markup=markup_inline_payment)

bot.polling()
