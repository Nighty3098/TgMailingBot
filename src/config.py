import loguru
import pretty_errors
from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.markdown import *
from aiogram.fsm.storage.memory import MemoryStorage
import os

"""
0 - admin
1 - user
"""

try:
    TOKEN = os.getenv("BOT_TOKEN")
    log_file = "logs/BOT.log"

    bot = Bot(TOKEN, storage=MemoryStorage())
    dp = Dispatcher()
    json_path = "data/data.json"
    json_name = "data.json"

    logger = loguru.logger

    logger.level("DEBUG", color="<green>")
    logger.level("INFO", color="<cyan>")
    logger.level("WARNING", color="<yellow>")
    logger.level("CRITICAL", color="<red>")

    logger.add(
        log_file,
        level="DEBUG",
        rotation="1000 MB",
        retention="31 days",
        backtrace=True,
        diagnose=True,
    )

    logger.debug(f"The bot launched successfully")
    logger.debug(f"Data: {json_path}")
except Exception as e:
    print(f"Error: {e}")