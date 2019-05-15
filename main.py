import requests
import telebot
import re

bot = telebot.TeleBot('840709555:AAEm3hTvuc3wwAuXOWuQZj8kqdVtJXoMQwY')
SITE = 'http://selet.biz'

def get_list_of_applications():
    r = requests.get(SITE)
    page = r.text
    proj = re.findall('id="bx_3218110189_\d{5}">.{1,}?<', page)
    proj = [re.findall('>.+<', p)[0][1:-1] for p in proj]
    return proj

def get_list_of_alans():
    r = requests.get(SITE + '/tat/projects/camp/')
    page = r.text
    camps = re.findall('<a href="(/tat/projects/camp/.+/)">(.+)</a>\n', page)[:19]
    return camps

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Заявки":
        res = "\n".join(get_list_of_applications())
    elif message.text == "Лагеря":
        res = "**" + str(get_list_of_alans()) + "**"        
    else:
        res = "__Я тебя не понимаю__"
    bot.send_message(message.from_user.id, res, parse_mode='Markdown')

print(get_list_of_alans())
        
bot.polling(none_stop=True, interval=0)
