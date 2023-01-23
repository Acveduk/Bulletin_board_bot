from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode, InlineKeyboardButton

from filters import CheckAdmins, CheckBan
from keyboards.default import keyboards
from loader import dp, bot
from states.states_users import Admin_Money, Buy, Admin_Ban, Admin_Message, User_Mes, Admin_Mes
from utils.db_api.postgres import add_money_user, check_balance


@dp.message_handler(CheckAdmins(), text='Пополнить баланс')
async def bot_start_admin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите ID пользователя</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Money.User.set()

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()

    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()

@dp.message_handler(text='Отмена', state=[Admin_Money.User, Admin_Money.Money])
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы вернулись в главное меню',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), state=Admin_Money.User)
async def bot_start_admin(message: types.Message, state: FSMContext):
    await state.update_data(users=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите кол-во денег</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Money.Money.set()


@dp.message_handler(CheckAdmins(), state=Admin_Money.Money)
async def bot_start_admin(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = data.get('users')
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Добавить', callback_data=f"plus:{user}:{message.text}")
            ],
            [
                InlineKeyboardButton(text=f'Отмена', callback_data="del")
            ]
        ]
    )
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>User:</i> {user}\n'
                                f'<i>Деньги:</i> {message.text}',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(text_contains='plus')
async def del_ad_d(call: types.CallbackQuery):
    list = call.data.split(":")[1::]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    check = await check_balance(user_id=int(list[0]))
    await add_money_user(user_id=int(list[0]), money=check[0]['money'] + int(list[1]))
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Деньги успешно добавлены!',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(text_contains='del')
async def del_ad_d(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Добавление денег отменено!',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
