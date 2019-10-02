import datetime
from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import TG_TOKEN
from echo.config import TG_API_URL


def do_start(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi.Send me smth')


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='List of all cmds is in Menu\n'
             'Also i will answer on your messages'
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = 'Yur ID = {}\n\n{}'.format(chat_id, update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=text, )


def do_time(bot: Bot, update: Update):
    """Узнать серверное время"""
    now = datetime.datetime.now()
    bot.send_message(
        chat_id=update.message.chat_id,
        text=now.strftime("%d-%m-%Y %H:%M:%S"),
    )


def main():
    bot = Bot(token=TG_TOKEN, base_url=TG_API_URL, )
    updater = Updater(bot=bot, )
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
