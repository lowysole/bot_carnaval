from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)

# List all menus

# Main menu
def define_main_menu():
    main_menu = [[InlineKeyboardButton('Programa', callback_data='programa')],
                 [InlineKeyboardButton('Cartell', callback_data='cartell')],
                 [InlineKeyboardButton('Video', callback_data='video')],
                 [InlineKeyboardButton('Següent', callback_data='next')]]
    return InlineKeyboardMarkup(main_menu)

def message_main_menu():
    return 'Que vols consultar?'
