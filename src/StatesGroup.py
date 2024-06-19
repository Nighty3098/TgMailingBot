from aiogram import *
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    main = State()
    wait_for_message = State()
    get_message = State()
    send_message = State()
    complete = State()