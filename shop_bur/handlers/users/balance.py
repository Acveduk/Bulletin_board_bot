import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode, InlineKeyboardButton
from pyqiwip2p import QiwiP2P

from filters import CheckBan
from keyboards.default import keyboards
from keyboards.inline.pay_keyboard import buy_menu
from loader import dp, bot
from states.states_users import Admin_Mes, User_Mes, Admin_Money, Admin_Message, Admin_Ban, Buy
from utils.db_api.postgres import check_balance, add_pay, get_pay, get_money, add_money_user, del_pay, del_pay2

p2p = QiwiP2P(
    auth_key="=")


@dp.message_handler(CheckBan(), text="💵 Баланс")
async def bot_start_user(message: types.Message):
    check = await check_balance(user_id=message.from_user.id)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'💳 Пополнить', callback_data='top')
            ]
        ]
    )
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'<b>Ваш баланс:</b> {check[0]["money"]} руб.\n'
                                f'<b>Кол-во заявок сегодня:</b> {check[0]["check_num"]} шт.\n\n'
                                f'<i>Стоимость публикации объявлений в течение суток:</i>\n'
                                f'1️⃣ <i>1-ый пост - 50 руб.</i>\n'
                                f'2️⃣ <i>2-ой пост и более  - 100 руб.</i>\n\n'
                                f'<i>* счетчик поданных объявлений обнуляется в 00:00 МСК⚠️</i>\n'
                                f'<i>** при нажатии <b>пополнить</b> прошлый счет анулируется</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()

@dp.callback_query_handler(CheckBan(), text_contains='top')
async def top(call: types.CallbackQuery):
    await del_pay2(user_id=call.from_user.id)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'💳 На 200 руб', callback_data='pay:1')
            ],
            [
                InlineKeyboardButton(text=f'💳 На 600 руб', callback_data='pay:2')
            ],
            [
                InlineKeyboardButton(text=f'💳 На 1000 руб', callback_data='pay:3')
            ]
        ]
    )
    await call.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(CheckBan(), text_contains='pay')
async def pay(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    price = call.data.split(":")[-1]
    if price[0] == '1':
        amount = 200
    elif price[0] == '2':
        amount = 600
    else:
        amount = 1000
    comment = str(call.from_user.id) + "_" + str(random.randint(1000, 9999))
    bill = p2p.bill(amount=amount, lifetime=30, comment=comment)

    await add_pay(user_id=call.from_user.id, money=amount, bill_id=str(bill.bill_id))

    await bot.send_message(chat_id=call.from_user.id,
                           text=f"Вам нужно отправить {amount} руб. на Наш счет Qiwi\n"
                                f"Ссылка: {bill.pay_url}\n\n"
                                f"Указав комментарий к оплате: <code>{comment}</code>",
                           reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id), parse_mode=ParseMode.HTML)


@dp.callback_query_handler(CheckBan(), text_contains='check_')
async def check(call: types.CallbackQuery):
    bill = str(call.data[6:])
    info = await get_pay(bill_id=bill)
    mon = await get_money(bill_id=bill)
    if info:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            user_money = await check_balance(user_id=call.from_user.id)
            money = int(mon[0]["money"])
            await add_money_user(user_id=call.from_user.id, money=user_money[0]["money"] + money)
            await del_pay(bill_id=bill)
            await call.message.delete()
            await bot.send_message(chat_id=call.from_user.id, text="Ваш счет пополнен!!!")
            await bot.send_message(chat_id=-1001863161367, text=f'<i>Пользователь:</i> <code>{call.from_user.id}</code>\n'
                                                                f'<i>Username:</i> @{call.from_user.username}\n'
                                                                f'<i>Ссылка:</i> tg://user?id={call.from_user.id}\n\n'
                                                                f"Оплатил: {money} руб", parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(chat_id=call.from_user.id, text="Вы не оплатили счет!!!",
                                   reply_markup=buy_menu(isUrl=False, bill=bill))
    else:
        await bot.send_message(chat_id=call.from_user.id, text="Счет не найден!!!")
