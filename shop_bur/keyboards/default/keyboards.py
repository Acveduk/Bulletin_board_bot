from aiogram import types


def keyboard_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📄 Создать объявление', '💵 Баланс')
    keyboard.row('👤 Перейти в чат', '📩 Техподдержка')
    return keyboard

def keyboard_start_admin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📄 Создать объявление', '💵 Баланс')
    keyboard.row('👤 Перейти в чат', '📩 Техподдержка')
    keyboard.row('Меню администратора')
    return keyboard

def keyboard_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('⬅ Главное меню')
    return keyboard