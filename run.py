
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

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
from backend import settings
from backend import menus as m

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PROGRAMA, CARTELL, VIDEO = range(3)

def inici(update, context):
    user = update.message.from_user
    logger.info("User {} entering to the BOT".format(user.first_name))
    update.message.reply_text(
        'Benvinguts al BOT de Carnaval!\n'
        'Aquest BIT et donarà tota la informació necessària per estar'
        'informat de tot el que passa a Tàrrega.\n'
        'Tecleja /menu per accedir al menú sempre que vulguis\n'
        'Envia /tancar per parar de parlar amb mi.\n\n')
    update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def start(update,context):
        inici(update,context)


def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())

def tancar(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Adeu! Si vols tornar a parlar amb mi, tecleja /inici',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Start
    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)
    updater.start_polling()

    inici_handler = CommandHandler('start', start)
    dp.add_handler(inici_handler)

    # Start Menu
    inici_handler = CommandHandler('menu', main_menu)
    dp.add_handler(inici_handler)
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))

    # Finish
    finish_handler = CommandHandler('tancar', tancar)
    dp.add_handler(finish_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
