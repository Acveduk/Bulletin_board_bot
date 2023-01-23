from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


class CheckAdmins(BoundFilter):
    async def check(self, message: types.Message) -> bool:

        if message.from_user.id in admins:
            return True
        else:
            return False