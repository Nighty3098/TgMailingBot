import asyncio

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.filters import callback_data
from aiogram.types import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import *
from requests.models import *

from data.get_data import *

async def create_admin_panel(user_id):
    if await get_user_role(user_id) == 0:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="Отправить пользователям сообщение", callback_data="send_message"))
        builder.adjust(1)

        logger.debug(f"Create admin panel")

        return builder.as_markup()

    else:
        logger.warning(f"{user_id} trying to open admin panel")