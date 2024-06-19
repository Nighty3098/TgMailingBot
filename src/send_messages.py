import asyncio

from data.get_data import *
from StatesGroup import *

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

async def send_messages(admin_message, state: FSMContext) -> None:
    try:
        data = await get_json_data()

        logger.debug(data["users"])


        for user in data["users"]:
            logger.debug(user)
            await bot.send_message(user, admin_message)
    except Exception as e:
        logger.error(f"Error: {e}")


async def send_messages_with_picture(file_id, caption, state: FSMContext) -> None:
    try:
        data = await get_json_data()
        
        logger.debug(data["users"])
        
        for user in data["users"]:
            logger.debug(user)
            await bot.send_photo(user, photo=file_id, caption=caption)
    except Exception as e:
        logger.error(f"Error: {e}")