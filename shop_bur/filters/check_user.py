from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.postgres import check_user, check_date

from data.config import admins


class CheckBan(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        date = datetime.now()
        await check_date(date=date.date())
        if await check_user(user_id=message.from_user.id):
            return False
        else:
            return True
