import asyncio
import json
import logging
import requests

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.filters import callback_data
from aiogram.types import *
from aiogram.types import message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import InputFile
from requests.models import *

from MESSAGES_TEXT import *
from StatesGroup import *
from data.get_data import *
from config import *
from kb_builder import *
from send_messages import *

@dp.message(CommandStart())
async def main_menu(message: Message, state: FSMContext) -> None:
    user_id = str(message.from_user.id)
    chat_id = message.chat.id
    member = await bot.get_chat_member(chat_id, user_id)
    username = member.user.username
    
    await add_new_user(user_id, username)
    user_role = await get_user_role(user_id)

    if user_role == 1:
        await message.answer(f"сәлем, қалайсың?")
        logger.info(f"User: {user_id}:{username} logged in")
    if user_role == 0:
        await state.update_data(admin_id=user_id, username=username)
        await state.set_state(Form.main)
        await message.answer(f"Привет, {username} - [ADMIN]", reply_markup=await create_admin_panel(user_id))
        logger.info(f"Admin: {user_id}:{username} logged in")

    data = await get_json_data()

@dp.callback_query(F.data == "send_message")
async def wait_for_message_from_admin(callback: types.CallbackQuery, state: FSMContext) -> None:
    try:
        data = await state.get_data()
        admin_id = data.get("admin_id")
        username = data.get("username")
        await state.set_state(Form.wait_for_message)
        await bot.send_message(admin_id, wait_message)
        logger.info(f"Admin: {admin_id}:{username} wants to send message to all users")
    except Exception as err:
        logger.error(f"{err}")

@dp.message(Form.wait_for_message)
async def get_message(message: Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()
        admin_id = data.get("admin_id")
        username = data.get("username")
        await state.set_state(Form.get_message)

        if message.photo:
            try:
                file_id = message.photo[-1].file_id
                file = await bot.get_file(file_id)
                file_url = file.file_path

                caption = message.caption
                logger.debug(f"Picture received: {file_url}")
                logger.info(f"Admin message: {caption}")

                await bot.send_message(admin_id, "Сообщение доставлено")
                await send_messages_with_picture(file_id, caption, state)
            except Exception as e:
                logger.error(f"Error: {e}")

            await main_menu(message, state)
        else:
            logger.debug('No pictures found')

            try:
                admin_message = str(message.text)
                logger.info(f"Admin message: {admin_message}")

                await send_messages(admin_message, state)
                await bot.send_message(admin_id, "Сообщение доставлено")
            except Exception as e:
                logger.error(f"Error: {e}")

            await main_menu(message, state)
        
    except Exception as e:
        logger.error(f"Error: {e}")
