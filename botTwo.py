import requests
import telebot
import random

url = "https://api.telegram.org/bot1603886447:AAGkAIDABghavkCleP8XMhEiCc1M1EPnFOg/getUpdates" # token
def last_update(request):
    responce = requests.get(request + "getUpdates")
    responce = responce.json()
    results = responce['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def get_message_text(update):
    message_text = update['message']['text']
    return message_text

def send_message(chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def main():
    update_id = last_update(url)['update_id']
    update = last_update(url)

    while True:

        if update_id == last_update(url)['update_id']:
            if get_message_text(update).lower() == 'привет' or get_message_text(update).lower() == 'здравствуйте' or get_message_text(update).lower() == 'добрый день':
                send_message(get_chat_id(update), 'Привет! Напиши "Играть", чтобы кинуть кость')
            elif get_message_text(update).lower() == 'играть':
                _1 = random.randint(1,6)
                _2 = random.randint(1,6)
                send_message(get_chat_id(update), 'Выпало' + str(_1) + 'и' + str(_2) + '\nТвой результат ' + str(_1 + _2))
            else:
                send_message(get_chat_id(update), 'Извините, я вас не понял')
                update_id += 1
if __name__ == '__main__':
    main()