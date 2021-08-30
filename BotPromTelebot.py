import telebot
import random

bot = telebot.TeleBot('1603886447:AAGkAIDABghavkCleP8XMhEiCc1M1EPnFOg')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Напиши "Играть", чтобы кинуть игральную кость')
    elif message.text.lower() == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'я тебя люблю':
        bot.send_sticker(message.chat.id, '1603886447:AAGkAIDABghavkCleP8XMhEiCc1M1EPnFOg')
    elif message.text.lower() == 'Играть':
        _1 = random.randint(1, 6)
        _2 = random.randint(1, 6)
        bot.send_message(message.chat.id, 'Выпало' + str(_1) + 'and' + str(_2) + '\nТвой результат' + str(_1 + _2))
    # else:
    #     bot.send_message(message.chat.id, 'Извините, я Вас не понял')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()