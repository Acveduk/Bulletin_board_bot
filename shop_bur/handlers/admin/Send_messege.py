from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ParseMode, ContentTypes

from filters import CheckAdmins, CheckBan
from keyboards.default import keyboards
from loader import dp, bot
from states.states_users import Admin_Message, Admin_Mes, User_Mes, Admin_Money, Admin_Ban, Buy
from utils.db_api.postgres import select_all_user


@dp.message_handler(CheckAdmins(), text='Написать всем')
async def admin_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Отмена')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Введите сообщения</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Message.Message.set()

@dp.message_handler(CheckBan(), CommandStart(), state=[Admin_Mes.Message1, Admin_Mes.Message2, User_Mes.Message1, User_Mes.Message2, Admin_Money.User, Admin_Money.Money, Admin_Message.Message, Admin_Message.Message2, Admin_Ban.Ban_On, Admin_Ban.Ban_Off, Buy.Text, Buy.Photo])
async def bot_start_user(message: types.Message, state: FSMContext):
    keyboard = keyboards.keyboard_start()
    await bot.send_message(chat_id=message.from_user.id,
                               text='<i>Вы вернулись в главное меню!</i>',
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()

@dp.message_handler(CheckAdmins(), text='Отмена', state=Admin_Message.Message)
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    await bot.send_message(chat_id=message.from_user.id,
                           text='Вы вернулись в меню администратора',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), state=Admin_Message.Message)
async def buy(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Отправить')
    keyboard.row('⬅ Назад')
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Нажмите отправить или прикрепите гиф/фото</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await Admin_Message.Message2.set()


@dp.message_handler(CheckAdmins(), text="Отправить", state=Admin_Message.Message2)
async def admin_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    data = await state.get_data()
    message1 = data.get('message')
    user_id = await select_all_user()
    count = 0
    for user in user_id:
        await bot.send_message(chat_id=user,
                               text=message1,
                               reply_markup=keyboard, parse_mode=ParseMode.HTML)
        count += 1
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваше сообщение успешно доставлено {count} людям',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), content_types=ContentTypes.ANIMATION, state=Admin_Message.Message2)
async def admin_message(message: types.Message, state: FSMContext):
    gif = message.animation.file_id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    data = await state.get_data()
    message1 = data.get('message')
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    user_id = await select_all_user()
    count = 0
    for user in user_id:
        await bot.send_animation(chat_id=user,
                                 animation=gif,
                                 caption=message1,
                                 reply_markup=keyboard, parse_mode=ParseMode.HTML)
        count += 1
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваше сообщение успешно доставлено {count} людям',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()


@dp.message_handler(CheckAdmins(), content_types=ContentTypes.PHOTO, state=Admin_Message.Message2)
async def admin_message(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    data = await state.get_data()
    message1 = data.get('message')
    keyboard.row('Написать всем', 'Написать одному')
    keyboard.row('Пополнить баланс', 'Бан')
    user_id = await select_all_user()
    count = 0
    for user in user_id:
        await bot.send_photo(chat_id=user,
                             photo=photo,
                             caption=message1,
                             reply_markup=keyboard, parse_mode=ParseMode.HTML)
        count += 1
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Ваше сообщение успешно доставлено {count} людям',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.finish()
