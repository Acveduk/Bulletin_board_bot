from aiogram import Dispatcher

from .check_admin import CheckAdmins
from .check_user import CheckBan


def setup(dp: Dispatcher):
    dp.filters_factory.bind(CheckAdmins)
    dp.filters_factory.bind(CheckBan)
