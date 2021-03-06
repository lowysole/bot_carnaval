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


from telegram import (Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardMarkup,InlineKeyboardButton)

from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Handler, Filters,
                          ConversationHandler, CallbackQueryHandler)

from backend import settings, easter
from backend import menus as m
from backend import emojis as emoji
from backend.database import query as q

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def inici(update, context):
    user = update.message.chat
    logger.info("User {}: {} {} entering to the BOT".format(
        user.username, user.first_name, user.last_name))
    full_name = str(user.first_name) + ' ' + str(user.last_name)
    db = q.Query(settings.DB_FILE)
    db.get_or_create_user(user.username, full_name)

    update.message.reply_text(
        '{} Benvinguts al BOT de Sa Majestat,'
        'Reina del Carnestoltes de Tàrrega! {} \n\n'
        'Aquest BOT et donarà tota la informació necessària per estar '
        'informat de tot el que passa a Tàrrega.\n\n'
        '{} Tecleja /menu per accedir al menú sempre que vulguis\n'
        '{} Envia /tancar per parar de parlar amb mi.\n\n'.format(
        emoji.festa, emoji.festa, emoji.carpeta, emoji.creu))
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
    update.message.reply_text(
        '{} Adeu! Si vols tornar a parlar amb mi, tecleja /inici'.format(
            emoji.adeu), reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="{} Ho sento, no t'he entès.\n\n"
        "{} Tecleja /menu per accedir al menú sempre que vulguis\n"
        "{} Envia /tancar per parar de parlar amb mi.\n\n".format(
        emoji.think, emoji.carpeta, emoji.creu))

def chat_message(update, context):
    text = update.message.text.lower()
    bot = context.bot
    answer_text = easter.message_answer(text)
    if answer_text[0] == 'text':
        bot.send_message(chat_id=update.message.chat_id,
                         text=answer_text[1])
    elif answer_text[0] == 'photo':
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=open(answer_text[1], 'rb'),
                       caption=answer_text[2])
    elif answer_text[0] == 'audio':
        bot.send_audio(chat_id=update.message.chat_id,
                       audio=open(answer_text[1], 'rb'))

# Menus
def main_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())


def programa_fisic(update, context):
    query = update.callback_query
    bot = context.bot
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Enviant Programa...")
    bot.send_document(chat_id=query.message.chat_id,
                      document=open('./backend/files/programa.pdf', 'rb'))
    menu(update, context)

def programa_online(update, context):
    query= update.callback_query
    bot = context.bot
    bot.send_message(chat_id=query.message.chat_id,
                     text="{} Tecleja /programa per consultar "
                     "per dia i hora els "
                     "esdeveniments propers d'aquest Carnestoltes.\n\n".format(
                          emoji.date))

def program_day(update, context):
    reply_keyboard = [['Dijous 20'],['Divendres 21'],
                      ['Dissabte 22'],['Diumenge 23']]
    update.message.reply_text(
        '{} Quin dia de la setmana vols consultar?'.format(emoji.lupa),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         one_time_keyboard=True))
    return 0

def program_hour(update,context):
    reply_keyboard = [['0', '1', '2', '3' ,'4' ,'5'],
                      ['6', '7', '8', '9' ,'10' ,'11'],
                      ['12', '13', '14', '15' ,'16' ,'17'],
                      ['18', '19', '20', '21' ,'22' ,'23']]
    db = q.Query(settings.DB_FILE)
    db.add_tmp_day(update.message.chat_id,
                   update.message.text)
    update.message.reply_text(
        "{} Quina hora vols consultar?".format(emoji.lupa),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    db.close()
    return 1

def program_query(update, context):
    query = update.callback_query
    bot = context.bot
    db = q.Query(settings.DB_FILE)
    args = []
    day = db.get_tmp_day(update.message.chat_id)[0][0]
    args.append(day)
    args.append(update.message.text)
    text = ''
    for row in db.process_query(args):
        template= "*{}*\n" \
            "{} {} | {}\n" \
            "{} _{}_\n\n".format(
                row[0], emoji.date, row[1], row[2], emoji.ubi, row[3])
        text = text + template
    if text == '':
        text = "{} No s'ha trobat cap esdeveniment" \
        "amb aquest horari.".format(emoji.creu)
    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode='Markdown')

    bot.send_message(chat_id=update.message.chat_id,
                     text='{} Tecleja /programa per tornar'
                     'a consultar un esdeveniment\n'
                     '{} Tecleja /menu per accedir al menú'.format(
                     emoji.carpeta, emoji.date))
    db.close()
    return ConversationHandler.END

def cartell_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Enviant cartell...")
    try:
        bot.send_photo(chat_id=query.message.chat_id,
                       photo=open('./backend/files/cartell.png', 'rb'),
                       timeout=60)
    except:
        bot.send_message(chat_id=query.message.chat_id,
                         text='Hem tingut problemes de connexió.\n'
                              'Torna-ho a provar més tard')
    menu(update, context)

def video_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                            text="Enviant vídeo...")
    bot.send_video(chat_id=query.message.chat_id,
                   video=open('./backend/files/video.mp4', 'rb'))
    menu(update, context)

def link_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_message(chat_id=query.message.chat_id,
                     text="{} *INSCRIPCIONS*\n\n"
                          "{} INSCRIPCIONS OBERTES AL "
                          "*SOPAR DEL CARNESTOLTES*, no et quedis sense!\n"
                          "http://bit.ly/SoparCARNA2020\n\n"
                          "{} INSCRIPCIONS OBERTES A LA "
                          "*RUA DE COMPARSES DEL CARNESTOLTES*\n"
                          "http://bit.ly/RuaComparsesCarnestoltes2020\n\n"
                          "{} Tota la informació i la resta d'inscripcions\n"
                          "http://www.carnestoltestarrega.cat/".format(
                              emoji.date, emoji.sopar,
                              emoji.dancer, emoji.info),
                     parse_mode='Markdown')
    menu(update, context)

def xarxes_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_message(chat_id=query.message.chat_id,
                     text="{} *INSTAGRAM*\n"
                          "https://www.instagram.com/carnavaltarrega\n\n"
                          "{} *FACEBOOK*\n"
                          "https://www.facebook.com/CarnestoltesTarrega\n\n"
                          "{} *TWITTER*\n"
                          "https://twitter.com/carnavaltarrega\n\n"
                          "{} *WEB*\n"
                          "www.carnestoltestarrega.cat\n\n".format(
                              emoji.camera, emoji.book,
                              emoji.twitter, emoji.web),
                     parse_mode='Markdown')
    menu(update, context)

def answer_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_message(chat_id=query.message.chat_id,
                     text='Holis, com estem?\n'
                     'He estat programada per respondre les teves '
                     'inquietuds més Targarines. Així que aifina bé '
                     'les teves preguntes!')

# Messages
def main_menu_message():
    return '{} Que vols consultar?'.format(emoji.lupa)

# Keyboards
def main_menu_keyboard():
    main_menu = [[InlineKeyboardButton('Cartell',
                                       callback_data='cartell'),
                  InlineKeyboardButton('Programa Físic',
                                       callback_data='programa_f')],
                 [InlineKeyboardButton('Vídeo',
                                       callback_data='video'),
                  InlineKeyboardButton('Programa Online',
                                       callback_data='programa_o')],
                 [InlineKeyboardButton('Inscripcions',
                                       callback_data='link'),
                  InlineKeyboardButton('Xarxes Socials',
                                       callback_data='xarxes')],
                 [InlineKeyboardButton('Conversa amb mi',
                                       callback_data='answer')]]
    return InlineKeyboardMarkup(main_menu, one_time_keyboard=True)

def back_menu_keyboard():
    back_menu = [[InlineKeyboardButton('Endarrere',
                                       callback_data='main_menu')]]
    return InlineKeyboardMarkup(back_menu)

def main(args):
    token = settings.DEV_TOKEN if args.dev_bot else settings.TOKEN

    # Initialize bot
    bot = Bot(token)
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Start Handler
    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    inici_handler = CommandHandler('inici', inici)
    dp.add_handler(inici_handler)

    # Menu Handler
    inici_handler = CommandHandler('menu', menu)
    dp.add_handler(inici_handler)
    dp.add_handler(CallbackQueryHandler(main_menu, pattern='main_menu'))
    dp.add_handler(CallbackQueryHandler(programa_fisic, pattern='programa_f'))
    dp.add_handler(CallbackQueryHandler(programa_online, pattern='programa_o'))
    dp.add_handler(CallbackQueryHandler(cartell_menu, pattern='cartell'))
    dp.add_handler(CallbackQueryHandler(video_menu, pattern='video'))
    dp.add_handler(CallbackQueryHandler(link_menu, pattern='link'))
    dp.add_handler(CallbackQueryHandler(xarxes_menu, pattern='xarxes'))
    dp.add_handler(CallbackQueryHandler(answer_menu, pattern='answer'))

    # Program Handler
    program_handler = ConversationHandler(
        entry_points=[CommandHandler('programa', program_day)],
        states={
            0: [MessageHandler(Filters.text, program_hour)],
            1: [MessageHandler(Filters.text, program_query)],
        },
        fallbacks=[CommandHandler('menu', menu)]
    )
    dp.add_handler(program_handler)

    # Finish
    finish_handler = CommandHandler('tancar', tancar)
    dp.add_handler(finish_handler)

    # Chat message
    chat_message_handler = MessageHandler(Filters.text, chat_message)
    dp.add_handler(chat_message_handler)
    # Incorrect command
    unknown_command_handler = MessageHandler(Filters.command, unknown_command)
    dp.add_handler(unknown_command_handler)

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
    args = parser.parse_args()
    main(args)
