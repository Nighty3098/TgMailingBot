import asyncio
import json

from config import *

async def get_json_data():
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
            logger.info(f"JSON DATA: {data}")
            return data

    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")

async def get_user_role(user_id):
    try:
        data = await get_json_data()
        
        if user_id in data["admins"]:
            return 0
        if user_id in data["users"]:
            return 1
        else:
            return 9

    except Exception as e:
        logger.error(f"Error JSON: {e}")

async def add_new_user(user_id, username):
    data = await get_json_data()

    if user_id in data["admins"] or user_id in data["users"]:
        logger.debug(f"The user is already in the database: {user_id} : {username}")
    else :
        try: 
            data["users"].append(user_id)

            with open(json_path, "w") as f:
                json.dump(data, f, indent=4)

            logger.debug(f"Added new user: {user_id} : {username}")
        except Exception as e:
            logger.error(f"Error JSON: {e}")