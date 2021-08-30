import json
import telebot
import datetime
#Добавить математика дата препод


def checkForAdmin(id):
    with open("admins.json", "r") as read_file:
        admins = json.load(read_file)
        return str(id) in admins["admins"]
def addMeeting(date,name,teacher):
    with open("meetings.json", "r") as read_file:
        meetings = json.load(read_file)
        id = meetings["meetings"][0]["id"]
        for i in meetings["meetings"]:
            if(id < int(i["id"])):
                id = int(i["id"])
        id+=1

        data={"id": id, "date": f"{date}", "name": f"{name}","Teacher": f"{teacher}", "persons": []}

        #data = json.dumps(data)
        meetings["meetings"].append(data)
        print(meetings)
        with open("meetings.json", "w") as write_file:
            json.dump(meetings, write_file)
        NotifyClients(id)
def checkMeeting(date):
    now = datetime.datetime.now()
    date = datetime.datetime.strptime(date[0: date.find("-")-1] , "%d.%m.%Y")
    return date < now

def deleteMeeting(id):
    with open("meetings.json" , "r") as read_file:
        meetings = json.load(read_file)

        for i in meetings["meetings"]:
            if(int(id) == int(i["id"])):
                meetings["meetings"].pop(int(id)-1)
                count = 1
                for i in meetings["meetings"]:
                    i["id"] = count
                    count+=1
                with open("meetings.json", "w") as write_file:
                    json.dump(meetings, write_file)
                return True
        return False

def NotifyClients(id):
    with open("meetings.json", "r") as read_file:
        meetings = json.load(read_file)
        for i in meetings["meetings"]:
            if str(id) == str(i["id"]):
                with open("clients.json", "r") as read_file:
                    clients = json.load(read_file)
                    for personId in clients["clients"]:
                        bot.send_message(personId,"У нас новое мероприятие" + i["name"] + " будет " + i["date"])
def add_client(id):
    with open("clients.json", "r") as read_file:
        clients = json.load(read_file)
        if id not in clients["clients"]:
            clients["clients"].append(str(id))
            with open("clients.json", "w") as write_file:
                json.dump(clients, write_file)
bot = telebot.TeleBot('1805152764:AAGFr6pVX7AM80v_JvufLb_JseUVHIbe-GI')
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.id}')
    add_client(str(message.from_user.id))
    checkMeeting(123)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    add_client(str(message.from_user.id))
    if message.text.lower() == 'привет' or message.text.lower() == 'здравствуйте':
        bot.send_message(message.from_user.id, 'Привет!')

    elif(message.text.lower() == 'мероприятия'):

        with open("meetings.json", "r") as read_file:
            meetings = json.load(read_file)
            for i in meetings["meetings"]:
                bot.send_message(message.from_user.id, "Мероприятие № " + str(i["id"]))
                bot.send_message(message.from_user.id, "Date - " + i["date"])
                bot.send_message(message.from_user.id, "Theme - " + i["name"])
                bot.send_message(message.from_user.id, "Name of Teacher - " + i["Teacher"])
    elif (message.text.lower().find("хочу") != -1):

        msg = message.text.lower().split()
        print(msg)
        with open("meetings.json", "r") as read_file:
            meetings = json.load(read_file)
            for i in meetings["meetings"]:
                if(msg[1] == str(i["id"])):
                    if( str(message.from_user.id) not in i["persons"]):
                        i["persons"].append(str(message.from_user.id))
                    break

            print(meetings)
            with open("meetings.json", "w") as write_file:
                json.dump(meetings, write_file)
    elif (message.text.lower() == '1234'):
        bot.send_message(message.from_user.id, "Вы админ")
        with open("admins.json", "r") as read_file:
            admins = json.load(read_file)
            if (str(message.from_user.id) not in admins["admins"]):
                admins["admins"].append(str(message.from_user.id))
                admins["count"] = int(admins["count"] + 1)
            with open("admins.json", "w") as write_file:
                json.dump(admins, write_file)
    elif(message.text.lower().find("добавить") != -1):
        if checkForAdmin(str(message.from_user.id)):
            msg = message.text.split("\n")
            print(msg)
            addMeeting(msg[1],msg[2],msg[3])

    elif(message.text.lower() == "рассылка"):
        with open("admins.json", "r") as read_file:
            admins = json.load(read_file)
            if (str(message.from_user.id)  in admins["admins"]):
                with open("meetings.json", "r") as read_file:
                    meetings = json.load(read_file)
                    for i in meetings["meetings"]:
                        for personId in i["persons"]:
                            bot.send_message(personId , "У вас встреча в " + i["date"])
            else:
                bot.send_message(message.from_user.id , "У вас нет прав админа")
    elif(message.text.lower().find("удалить") != -1):
        print(checkForAdmin(message.from_user.id))
        msg = message.text.lower().split()
        if(checkForAdmin(message.from_user.id)):
            if(deleteMeeting(msg[1])):
                bot.send_message(message.from_user.id, "Удалилось мероприятие " )
            else:
                bot.send_message(message.from_user.id, "Такого мероприятия нет, вы ошиблись ID")
        else:
            bot.send_message(message.from_user.id, "Вы не админ " )
    elif(message.text.lower().find("редактировать") != -1 ):
        msg = message.text.lower().split("\n")
        id = msg[0].split()[1]
        with open("meetings.json", "r") as read_file:
            meetings = json.load(read_file)
            for i in meetings["meetings"]:
                if(int(id) == i["id"]):
                    i["date"] = msg[1]
                    i["name"] = msg[2]
                    i["Teacher"] = msg[3]
                    bot.send_message(message.from_user.id, "Успешно изменили № " + str(id))
                    with open("meetings.json", "w") as write_file:
                        json.dump(meetings, write_file)
    elif(message.text.lower() == "актуальность"):
        with open("meetings.json", "r") as read_file:
            meetings = json.load(read_file)
            for i in meetings["meetings"]:
                if(checkMeeting(i["date"])):
                    bot.send_message(message.from_user.id, "Устарело №"+ str(i["id"]))

    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
bot.polling(none_stop=True)