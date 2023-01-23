from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode

from filters import CheckAdmins, CheckBan
from keyboards.default import keyboards
from loader import dp, bot
from states.states_users import Admin_Ban, Admin_Mes, User_Mes, Admin_Money, Admin_Message, Buy
from utils.db_api.postgres import add_user_ban, del_user_ban


@dp.message_handler(CheckAdmins(), text='Бан')
async def admin_ban(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Забанить')
    keyboard.row('Разбанить')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Выберите действие</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), text='Забанить')
async def admin_ban(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Отмена')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите ID ользователя</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Ban.Ban_On.set()


@dp.message_handler(CheckAdmins(), text='Разбанить')
async def admin_ban(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Отмена')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите ID ользователя</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Ban.Ban_Off.set()


@dp.message_handler(CheckAdmins(), text='Отмена', state=[Admin_Ban.Ban_On, Admin_Ban.Ban_Off])
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы вернулись в меню администратора',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), state=Admin_Ban.Ban_On)
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    check = await add_user_ban(user_id=int(message.text))
    if check:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Пользователь c id {message.text} забанен',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Пользователь c id {message.text} был забанен ранее',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), state=Admin_Ban.Ban_Off)
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    check = await del_user_ban(user_id=int(message.text))
    if check:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Пользователь c id {message.text} разбанен',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Пользователь c id {message.text} не был забанен ранее',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()
