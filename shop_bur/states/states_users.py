from aiogram.dispatcher.filters.state import State, StatesGroup


class Buy(StatesGroup):
    Photo = State()
    Text = State()


class Admin_Ban(StatesGroup):
    Ban_On = State()
    Ban_Off = State()


class Admin_Message(StatesGroup):
    Message = State()
    Message2 = State()

class Admin_Mes(StatesGroup):
    Message1 = State()
    Message2 = State()

class User_Mes(StatesGroup):
    Message1 = State()
    Message2 = State()

class Admin_Money(StatesGroup):
    User = State()
    Money = State()
