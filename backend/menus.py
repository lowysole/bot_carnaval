from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

# List all menus

# Menus
def main_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=main_menu_message(),
                          reply_markup=main_menu_keyboard())

def program_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=program_menu_message(),
                          reply_markup=program_menu_keyboard())

def cartell_menu(update, context):
    query = update.callback_query
    bot = context.bot
    bot.send_photo(chat_id=chat_id, photo=open('backend/files/cartell.jpg', 'rb'))
    bot.edit_message_text(chad_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=back_menu_keyboard())

# Messages
def main_menu_message():
    return 'Que vols consultar?'

def program_menu_message():
    return 'Descarrega el programa en format .pdf o consulta per hora '\
            'i dia les activitats del Carnaval'

# Keyboards
def main_menu_keyboard():
    main_menu = [[InlineKeyboardButton('Programa', callback_data='program')],
                 [InlineKeyboardButton('Cartell', callback_data='cartell')],
                 [InlineKeyboardButton('Video', callback_data='video')],
                 [InlineKeyboardButton('Següent', callback_data='next')]]
    return InlineKeyboardMarkup(main_menu)

def program_menu_keyboard():
    program_menu = [[InlineKeyboardButton('Programa físic', callback_data='programa_f')],
                 [InlineKeyboardButton('Programa on-line', callback_data='programa_o')],
                 [InlineKeyboardButton('Endarrere', callback_data='main')]]
    return InlineKeyboardMarkup(program_menu)

def back_menu_keyboard():
    back_menu_menu = [[InlineKeyboardButton('Endarrere', callback_data='main')]]
    return InlineKeyboardMarkup(back_menu)
