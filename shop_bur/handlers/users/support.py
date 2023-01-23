from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode, InlineKeyboardButton

from filters import CheckAdmins, CheckBan
from keyboards.default import keyboards
from keyboards.default.keyboards import keyboard_start
from loader import dp, bot
from states.states_users import User_Mes, Admin_Mes, Admin_Money, Admin_Message, Admin_Ban, Buy
from utils.db_api.postgres import add_money_user


@dp.message_handler(CheckBan(), text='📩 Техподдержка')
async def bot_start_admin(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Отмена")
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите описание своей проблемы</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await User_Mes.Message1.set()

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()

@dp.message_handler(CheckBan(), text='Отмена', state=User_Mes.Message1)
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы вернулись в главное меню',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckBan(), state=User_Mes.Message1)
async def bot_start_admin(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Отправить', callback_data=f"mes:{message.text}")
            ],
            [
                InlineKeyboardButton(text=f'Отмена', callback_data="naz")
            ]
        ]
    )
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<i>Текст:\n</i> {message.text}',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.callback_query_handler(CheckBan(), text_contains='mes')
async def del_ad_d(call: types.CallbackQuery):
    list = call.data.split(":")[1::]
    keyboard = keyboard_start()
    await bot.send_message(chat_id=-1001863161367,
                           text=f'<i>User:</i> <code>{call.from_user.id}</code>\n'
                                f'<i>Username:</i> @{call.from_user.username}\n'
                                f'<i>Ссылка:</i> tg://user?id={call.from_user.id}\n\n'
                                f'<i>Текст:\n</i> {list[0]}', parse_mode=ParseMode.HTML)
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id,
                           text="Сообщение отправлено! Ждите ответ в боте", reply_markup=keyboard,
                           parse_mode=ParseMode.HTML)


@dp.callback_query_handler(CheckBan(), text_contains='naz')
async def del_ad_d(call: types.CallbackQuery):
    keyboard = keyboard_start()
    await call.message.delete()
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'Сообщение не отправлено',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
