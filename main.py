import requests
import telegram
from telegram import ParseMode
import telebot
import re


bot = telebot.TeleBot('840709555:AAEm3hTvuc3wwAuXOWuQZj8kqdVtJXoMQwY')
SITE = 'http://selet.biz'

def get_list_of_applications():
    r = requests.get(SITE)
    page = r.text 
    app = re.findall(r'<a href="(/form/\?ID=\d{5})" class="btn" id="bx_3218110189_\d{5}">(.+)</a>', page)

    for i in range(len(app)):
        pos = app[i][1].find('style')
        app[i] = list(app[i])
        if pos >= 0:
            app[i][1] = app[i][1][:pos-1]
    return app

def get_list_of_camps():
    r = requests.get(SITE + '/tat/projects/camp/')
    page = r.text
    camps = re.findall('<a href="(/tat/projects/camp/.+/)">(.+)</a>\n', page)[:19]
    return camps

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Заявки":
        res = ""
        for addr, name in get_list_of_applications():
            res += '(' + name + ')[' + SITE + addr + '] \n'
    elif message.text == "Лагеря":
        res = ""
        for addr, name in get_list_of_camps():
            res += '(' + name + ')[' + SITE + addr + '] \n'
    else:
        res = "__Я тебя не понимаю__"
    bot.send_message(message.from_user.id, res, parse_mode='Markdown')
        
bot.polling(none_stop=True, interval=0)
