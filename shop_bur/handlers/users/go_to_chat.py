from filters import CheckBan
from keyboards.default import keyboards
from aiogram import types
from aiogram.types import ParseMode, InlineKeyboardButton
from loader import dp, bot


@dp.message_handler(CheckBan(), text="👤 Перейти в чат")
async def go_to_chat(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'👤 Ссылка на чат', url='https://t.me/BIRYLEVO_VZ_ADS_CHAT')
            ],
            [
                InlineKeyboardButton(text=f'👤 Ссылка на канал', url='https://t.me/BIRYLEVO_VZ_ADS_CHANNEL')
            ],
            [
                InlineKeyboardButton(text=f'👤 Ссылка на сайт', url='https://TAPLINK.CC/BIRYLEVO_VZ_ADS')
            ]
        ]
    )
    await bot.send_message(chat_id=message.from_user.id,
                           text='<i>Полезные ссылки</i>',
                           reply_markup=keyboard, parse_mode=ParseMode.HTML)