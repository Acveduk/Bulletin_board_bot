from aiogram.dispatcher.filters import CommandStart
from typing import List

from aiogram import types
from aiogram.types import ParseMode, InlineKeyboardButton, ContentTypes, MediaGroup

from filters import CheckBan
from keyboards.default import keyboards
from keyboards.default.keyboards import keyboard_start
from loader import dp, bot
from states.states_users import Buy, Admin_Mes, User_Mes, Admin_Money, Admin_Message, Admin_Ban
from aiogram_media_group import MediaGroupFilter, media_group_handler
from aiogram.dispatcher import FSMContext

from utils.db_api.postgres import check_balance, update_user_money_check, add_ad, check_ad, del_ad


@dp.message_handler(CheckBan(), text="📄 Создать объявление")
async def buy(message: types.Message):
    ad = await check_ad(user_id=message.from_user.id)
    if len(ad) > 0:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'<b>У Вас есть созданная заявка!!</b>\n'
                                    f'<i>Отправьте ее или отмените!</i>',
                               parse_mode=ParseMode.HTML)
        if ad[0]["check_media"] == "photo":
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f'Отправить', callback_data='send:photo')
                    ],
                    [
                        InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                    ]
                ]
            )
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
        elif ad[0]["check_media"] == "video":
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f'Отправить', callback_data='send:video')
                    ],
                    [
                        InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                    ]
                ]
            )
            await bot.send_video(chat_id=message.from_user.id,
                                 video=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f'Отправить', callback_data='send:gif')
                    ],
                    [
                        InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                    ]
                ]
            )
            await bot.send_animation(chat_id=message.from_user.id,
                                     animation=ad[0]["media"],
                                     caption=ad[0]["text"],
                                     reply_markup=keyboard)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('⬅ Назад')
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Пришлите от 1 фото, видео или GIF:</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await Buy.Photo.set()


@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckBan(), content_types=ContentTypes.VIDEO, state=Buy.Photo)
async def buy_photo(message: types.Message, state: FSMContext):
    photo = message.video.file_id
    list = [photo]
    await state.update_data(photo_group=list, check='video')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('⬅ Назад')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите описание:</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Buy.Text.set()


@dp.message_handler(CheckBan(), content_types=ContentTypes.PHOTO, state=Buy.Photo)
async def buy_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    list = [photo]
    await state.update_data(photo_group=list, check='photo')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('⬅ Назад')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите описание:</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Buy.Text.set()


@dp.message_handler(CheckBan(), content_types=ContentTypes.ANIMATION, state=Buy.Photo)
async def buy_photo(message: types.Message, state: FSMContext):
    gif = message.animation.file_id
    list = [gif]
    await state.update_data(photo_group=list, check='gif')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('⬅ Назад')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите описание:</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Buy.Text.set()


@dp.message_handler(CheckBan(), text="⬅ Назад", state=[Buy.Photo, Buy.Text])
async def back(message: types.Message, state: FSMContext):
    stateOld = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    stateOld = await stateOld.get_state()
    print(stateOld)
    if stateOld == 'Buy:Photo':
        keyboard = keyboards.keyboard_start()
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await state.finish()
    elif stateOld == 'Buy:Text':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('⬅ Назад')
        await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Пришлите от 1 фото, видео или GIF:</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await Buy.Photo.set()


@dp.message_handler(CheckBan(), content_types=['text'], state=Buy.Text)
async def buy_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    photo = data.get('photo_group')
    check = data.get('check')
    keyboard1 = keyboard_start()

    if check == "photo":
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f'Отправить', callback_data='send:photo')
                ],
                [
                    InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                ]
            ]
        )
        await add_ad(user_id=message.from_user.id, media=photo[0], text=text, check_media="photo")
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"<i>Объявление создано</i>",
                               reply_markup=keyboard1,
                               parse_mode=ParseMode.HTML)
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo[0],
                             caption=f"{text}",
                             reply_markup=keyboard)
    elif check == "video":
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f'Отправить', callback_data='send:video')
                ],
                [
                    InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                ]
            ]
        )
        await add_ad(user_id=message.from_user.id, media=photo[0], text=text, check_media="video")
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"<i>Объявление создано</i>",
                               reply_markup=keyboard1,
                               parse_mode=ParseMode.HTML)
        await bot.send_video(chat_id=message.from_user.id,
                             video=photo[0],
                             caption=f"{text}",
                             reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f'Отправить', callback_data='send:gif')
                ],
                [
                    InlineKeyboardButton(text=f'Отменить', callback_data='back:')
                ]
            ]
        )
        await add_ad(user_id=message.from_user.id, media=photo[0], text=text, check_media="gif")
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"<i>Объявление создано</i>",
                               reply_markup=keyboard1,
                               parse_mode=ParseMode.HTML)
        await bot.send_animation(chat_id=message.from_user.id,
                                 animation=photo[0],
                                 caption=f"{text}",
                                 reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(CheckBan(), text_contains='back')
async def del_ad_d(call: types.CallbackQuery):
    await del_ad(user_id=call.from_user.id)
    await call.message.delete()


@dp.callback_query_handler(CheckBan(), text_contains='send')
async def order_send(call: types.CallbackQuery):
    balance = await check_balance(user_id=call.from_user.id)
    ad = await check_ad(user_id=call.from_user.id)
    if balance[0]['money'] >= 50 and balance[0]['check_num'] == 0:
        money = balance[0]['money'] - 50
        check = balance[0]['check_num'] + 1
        await update_user_money_check(user_id=call.from_user.id, money=money, check_num=check)
        await call.message.answer(
            text=f"<i>Объявление отправлено в канал</i> - @BIRYLEVO_VZ_ADS_CHANNEL\n"
                 f"<i>С Вас снятно</i> <b>50 руб</b> <i>за первый пост за сегодня!</i>", parse_mode=ParseMode.HTML)
        if ad[0]["check_media"] == "photo":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_photo(chat_id=-1001646551793,
                                 photo=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
        elif ad[0]["check_media"] == "video":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_video(chat_id= -1001646551793,
                                 video=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_animation(chat_id= -1001646551793,
                                     animation=ad[0]["media"],
                                     caption=ad[0]["text"],
                                     reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
    elif balance[0]['money'] >= 100 and balance[0]['check_num'] >= 1:
        money = balance[0]['money'] - 100
        check = balance[0]['check_num'] + 1
        await update_user_money_check(user_id=call.from_user.id, money=money, check_num=check)
        await call.message.answer(
            text=f"<i>Объявление отправлено в канал</i> - @BIRYLEVO_VZ_ADS_CHANNEL\n"
                 f"<i>С Вас снятно</i> <b>100 руб</b> <i>за второй или более пост за сегодня!</i>",
            parse_mode=ParseMode.HTML)
        if ad[0]["check_media"] == "photo":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_photo(chat_id= -1001646551793,
                                 photo=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
        elif ad[0]["check_media"] == "video":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_video(chat_id= -1001646551793,
                                 video=ad[0]["media"],
                                 caption=ad[0]["text"],
                                 reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.row(
                types.InlineKeyboardButton(text="Написать автору", url=f't.me/{call.from_user.username}'))
            keyboard.row(
                types.InlineKeyboardButton(text="Разместить объявление", url=f't.me/byrulevo_vz_bot/?start=hello'))
            await bot.send_animation(chat_id= -1001646551793,
                                     animation=ad[0]["media"],
                                     caption=ad[0]["text"],
                                     reply_markup=keyboard)
            await del_ad(user_id=call.from_user.id)
    else:
        await call.message.answer(
            text=f"<i>Объявление не отправлено в канал</i> - @BIRYLEVO_VZ_ADS_CHANNEL\n"
                 f"<b>Ндостаточно средств! Пополните свой баланс.</b>", parse_mode=ParseMode.HTML)
