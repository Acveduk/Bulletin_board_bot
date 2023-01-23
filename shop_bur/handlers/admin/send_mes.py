from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode, InlineKeyboardButton

from filters import CheckAdmins, CheckBan
from keyboards.default import keyboards
from loader import dp, bot
from states.states_users import Admin_Money, Admin_Mes, User_Mes, Admin_Message, Admin_Ban, Buy
from utils.db_api.postgres import add_money_user


@dp.message_handler(CheckAdmins(), text='Написать одному')
async def bot_start_admin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите ID пользователя</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Mes.Message1.set()

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()

@dp.message_handler(CheckAdmins(), text='Отмена', state=[Admin_Mes.Message1, Admin_Mes.Message2])
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы вернулись в меню администратора',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), state=Admin_Mes.Message1)
async def bot_start_admin(message: types.Message, state: FSMContext):
    await state.update_data(user_mes=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите текст</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Mes.Message2.set()


@dp.message_handler(CheckAdmins(), state=Admin_Mes.Message2)
async def bot_start_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = data.get('user_mes')
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Отправить', callback_data=f"otpr:{user}:{message.text}")
            ],
            [
                InlineKeyboardButton(text=f'Отмена', callback_data="no")
            ]
        ]
    )
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>User:</i> {user}\n'
                                f'<i>Текст:</i> {message.text}',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(text_contains='otpr')
async def del_ad_d(call: types.CallbackQuery):
    list = call.data.split(":")[1::]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=int(list[0]),
                           text=f'{list[1]}',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await call.message.edit_text(text=f'Сообщение отправлено')


@dp.callback_query_handler(text_contains='del')
async def del_ad_d(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Сообщение не отправлено',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
