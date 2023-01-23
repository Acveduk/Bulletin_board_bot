from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode

from filters import CheckAdmins
from loader import dp, bot


@dp.message_handler(CheckAdmins(), text='/admin')
async def bot_start_admin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Выберите нужное действие</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
