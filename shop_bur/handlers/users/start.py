from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode

from filters import CheckBan
from keyboards.default import keyboards
from loader import dp, bot
from states.states_users import Admin_Mes, User_Mes, Admin_Money, Admin_Message, Admin_Ban, Buy
from utils.db_api.postgres import add_user_in_database


@dp.message_handler(CheckBan(), CommandStart())
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    check = await add_user_in_database(user_id=message.from_user.id, username=message.from_user.username,
                                       name=message.from_user.first_name)
    if check:
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Добро пожаловать!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Добро пожаловать!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckBan(), text="⬅ Главное меню")
async def main_menu(message: types.Message):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Вы вернулись в главное меню</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
