from telebot import TeleBot, types
from telegram import ParseMode

from queries.applications import ApplicationsView
from queries.projects import ProjectsView
from queries.camps import CampsView

from utils import list_of_links
from constants import CAMPS_KEYWORDS_NAMES
import constants

token = open('tgtoken.txt', 'r').readline().strip()
bot = TeleBot(token)


class Handler:
    standart_keyboard = types.ReplyKeyboardMarkup()
    standart_keyboard.row('Лагеря')
    standart_keyboard.row('Заявки')
    standart_keyboard.row('Проекты')
    standart_keyboard.row('🍚', '👍', '❤')

    pagination_keyboard = types.InlineKeyboardMarkup()
    prev_button = types.InlineKeyboardButton(text='⬅️', callback_data="prev")
    cur_button = types.InlineKeyboardButton(text='⚪️', callback_data="cur")
    next_button = types.InlineKeyboardButton(text='➡️', callback_data="next")
    pagination_keyboard.row(prev_button, cur_button, next_button)

    @staticmethod
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.send_message(message.chat.id, constants.START_MESSAGE, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=Handler.standart_keyboard)

    @staticmethod
    @bot.message_handler(commands=['help'])
    def help_command(message):
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
        keyboard.add(callback_button)
        bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)
        bot.send_message(message.chat.id, constants.HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN,
                         reply_markup=Handler.standart_keyboard)

    @staticmethod
    @bot.message_handler(func=lambda m: m.text.lower() in constants.CAMPS_KEYWORDS)
    def camps_pagination(message):
        res = list_of_links(CampsView.list())
        bot.send_message(message.chat.id, res,
                         parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True,
                         reply_markup=Handler.pagination_keyboard)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    def camps_callback(call):
        if call.data == 'cur':
            return
        if call.data == 'next':
            text = CampsView.next()
        else:
            text = CampsView.prev()
        bot.edit_message_text(text=text, reply_markup=Handler.pagination_keyboard,
                              parse_mode=ParseMode.MARKDOWN,
                              chat_id=call.message.chat.id, message_id=call.message.message_id)

    @staticmethod
    @bot.message_handler(func=lambda m: m.text in constants.STICKER_KEYWORDS)
    def get_sticker(message):
        user_id = message.chat.id
        text = message.text.lower()

        if text in constants.BON_APPETITE_KEYWORDS:
            sticker = constants.STICKER_ID['bon appetite']
        elif text in constants.COOL_KEYWORDS:
            sticker = constants.STICKER_ID['cool']
        elif text in constants.LOVE_KEYWORDS:
            sticker = constants.STICKER_ID['love']

        bot.send_sticker(user_id, sticker)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def text_messages(message):
        text = message.text.lower()
        user_id = message.chat.id

        if text in CAMPS_KEYWORDS_NAMES:
            res = CampsView.camp_detail(CAMPS_KEYWORDS_NAMES[text])

        elif text in constants.APPLICATIONS_KEYWORDS:
            res = list_of_links(ApplicationsView.list())

        elif text in constants.PROJECTS_KEYWORDS:
            res = list_of_links(ProjectsView.list())

        else:
            res = constants.DO_NOT_UNDERSTAND_MESSAGE

        bot.send_message(user_id, res, parse_mode=ParseMode.MARKDOWN,
                         disable_web_page_preview=True,
                         reply_markup=Handler.standart_keyboard)


@staticmethod
@bot.message_handler(content_types=['audio', 'video', 'document', 'location', 'contact', 'sticker'])
def unsupported_messages(message):
    res = f'_Я не умею отвечать на сообщения такого типа: {message.content_type}_'
    bot.send_message(message.from_user.id, res, parse_mode=ParseMode.MARKDOWN)


bot.polling(none_stop=True, interval=0)
