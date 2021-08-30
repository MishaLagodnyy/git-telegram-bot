import telebot

token = '1805152764:AAGFr6pVX7AM80v_JvufLb_JseUVHIbe-GI'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['post'])
def command(message):
    print(message.text.split(" ")[0])
    if message.text.split(" ")[0] == "/post":
        bot.send_message(message.chat.id, message.text.split(" ")[0])


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    print(message.new_chat_members[0].first_name)
    user_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, f"Welcome, {user_name}!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
