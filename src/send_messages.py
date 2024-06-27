import asyncio
import requests

from data.get_data import *
from StatesGroup import *

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import *

async def send_messages(admin_message, state: FSMContext) -> None:
    try:
        data = await get_json_data()

        logger.debug(data["users"])


        for user in data["users"]:
            try:
                logger.debug(user)
                response = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": user, "text": admin_message})
                # await bot.send_message(user, admin_message, allow_sending_without_reply=True)
            except Exception as e:
                logger.error(f"user:{user} Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")


async def send_messages_with_picture(file_id, caption, state: FSMContext) -> None:
    try:
        data = await get_json_data()
        
        logger.debug(data["users"])
        
        for user in data["users"]:
            try:
                logger.debug(user)
                response = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup",
                    json={
                        "chat_id": user,
                        "media": [
                            {"type": "photo", "media": file_id, "caption": caption}
                        ]
                    }
                )
                # await bot.send_photo(user, photo=file_id, caption=caption, allow_sending_without_reply=True)
            except Exception as e:
                logger.error(f"user:{user} Error: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")