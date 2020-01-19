# coding=utf-8
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import argparse


from telegram import Bot, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

from backend import settings
from backend import menus as m

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def inici(update, context):
    user = update.message.chat.username
    logger.info("User {} entering to the BOT".format(user))
    update.message.reply_text(
        'Benvinguts al BOT de Carnaval!\n'
        'Aquest BOT et donarà tota la informació necessària per estar '
        'informat de tot el que passa a Tàrrega.\n'
        'Tecleja /menu per accedir al menú sempre que vulguis\n'
        'Envia /tancar per parar de parlar amb mi.\n\n')
    menu(update, context)

def start(update, context):
    inici(update, context)

def menu(update, context):
    try:
        chat_id = update.callback_query.message.chat_id
    except:
        chat_id = update.message.chat_id
    bot = context.bot
    bot.send_message(chat_id=chat_id,
                     text=main_menu_message(),
                     reply_markup=main_menu_keyboard())

def tancar(update, context):
    user = update.message.chat.username
    logger.info("User %s canceled the conversation.", user)
    update.message.reply_text('Adeu! Si vols tornar a parlar amb mi, tecleja /inici',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ho sento, no t'he entès.\n"
        "Tecleja /menu per accedir al menú sempre que vulguis\n"
        "Envia /tancar per parar de parlar amb mi.\n\n")

# Menus
def main_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())

#def program_menu(update, context):
#    query = update.callback_query
#    bot = context.bot
#    bot.edit_message_text(chat_id=query.message.chat_id,
#                          message_id=query.message.message_id,
#                          text=program_menu_message(),
#                          reply_markup=program_menu_keyboard())
#
def programa_fisic(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_document(chat_id=query.message.chat_id,
                      document=open('./backend/files/dummy.pdf', 'rb'))
    menu(update, context)

def programa_online(update, context):
    query= update.callback_query
    bot = context.bot
    bot.send_message(chat_id=query.message.chat_id,
                     text="Tecleja /programa [dia] [hora] per veure la programació "
                          "del dia a partir de l'hora indicada\n"
                          "Exemple: /programa dissabte 17")

def cartell_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Enviant cartell...")
    bot.send_photo(chat_id=query.message.chat_id,
                   photo=open('./backend/files/dummy.jpg', 'rb'))
    menu(update, context)

def video_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Enviant video...")
    bot.send_video(chat_id=query.message.chat_id,
                   video=open('./backend/files/dummy.mp4', 'rb'))
    menu(update, context)

def link_menu(update, context):
    pass

# Messages
def main_menu_message():
    return 'Que vols consultar?'

# Keyboards
def main_menu_keyboard():
    main_menu = [[InlineKeyboardButton('Cartell', callback_data='cartell'),
                  InlineKeyboardButton('Programa Físic', callback_data='programa_f')],
                 [InlineKeyboardButton('Video', callback_data='video'),
                  InlineKeyboardButton('Programa Online', callback_data='programa_o')],
                 [InlineKeyboardButton('Inscripcions', callback_data='link')]]
    return InlineKeyboardMarkup(main_menu, one_time_keyboard=True)

def back_menu_keyboard():
    back_menu = [[InlineKeyboardButton('Endarrere', callback_data='main_menu')]]
    return InlineKeyboardMarkup(back_menu)

def main(args):
    token = settings.DEV_TOKEN if args.dev_bot else settings.TOKEN
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    bot = Bot(token)

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Start
    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    inici_handler = CommandHandler('inici', inici)
    dp.add_handler(inici_handler)

    # Start Menu
    inici_handler = CommandHandler('menu', menu)
    dp.add_handler(inici_handler)
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main_menu'))
    #dp.add_handler(CallbackQueryHandler(program_menu, pattern='program'))
    dp.add_handler(CallbackQueryHandler(programa_fisic, pattern='programa_f'))
    dp.add_handler(CallbackQueryHandler(programa_online, pattern='programa_o'))
    dp.add_handler(CallbackQueryHandler(cartell_menu, pattern='cartell'))
    dp.add_handler(CallbackQueryHandler(video_menu, pattern='video'))
    dp.add_handler(CallbackQueryHandler(link_menu, pattern='link'))


    # Finish
    finish_handler = CommandHandler('tancar', tancar)
    dp.add_handler(finish_handler)
    # Incorrect command
    unknown_handler = MessageHandler(Filters.command, unknown)
    dp.add_handler(unknown_handler)
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument('--dev-bot', dest='dev_bot', action='store_true',
                        help='Execute dev BOT')
    parser.add_argument('--dev-message', dest='dev_msg', action='store_true',
                        help='Execute dev message')
    args = parser.parse_args()
    main(args)
