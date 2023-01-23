from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQiwi = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(btnUrlQiwi)

    btnCheckQiwi = InlineKeyboardButton(text="Проверить оплату", callback_data="check_"+bill)
    qiwiMenu.insert(btnCheckQiwi)
    return qiwiMenu