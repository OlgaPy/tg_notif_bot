import asyncio
import json
import logging

import aiogram

import database.db_actions
from telegram import bot


def ms_problems_callback(redis_message: dict) -> None:
    """
    Sending the message from redis-message to telegram-user by login
    """
    json_redis_message = json.loads(redis_message['data'])
    tg_ids = database.db_actions.get_tg_ids_by_ms_login(ms_login=json_redis_message.get('username'))

    for tg_id in tg_ids:
        asyncio.create_task(bot.send_message(
            chat_id=tg_id,
            text=json_redis_message.get('message'),
            parse_mode=aiogram.types.ParseMode.HTML
        ))
        logging.info(f'Message: {json_redis_message.get("message")} was sent {tg_id}')
