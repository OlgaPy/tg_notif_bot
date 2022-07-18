import logging
import re
import traceback
from datetime import datetime

import aiogram

import settings
from database import db_actions
from . import _messages


def safe_try(input_func):
    async def wrapped(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
        try:
            await input_func(message, state)
        except Exception:
            response = _messages.TgMessages.CONTACT_ADMINISTRATOR.value.format(
                ex=f'{traceback.format_exc()}', email=settings.DataBase().mail_administrator
            )
            await message.reply(response)
            logging.info([response, message.from_user.id])
    return wrapped


def check_login_format(input_func):
    """
    Decorator for checking ms-login format
    :param input_func: reference to async function
    """
    async def wrapped(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
        """
        Async function for checking ms-login format
        :return: call function or None
        """

        success = False
        ms_login = message.get_args()
        if ms_login and re.search(r"^[a-z]\.[a-z]+$", ms_login, re.M | re.S) is not None:
            success = True
            await input_func(message,  state)
        else:
            await message.reply(
                _messages.TgMessages.INCORRECT_LOGIN.value
            )
            logging.info([_messages.TgMessages.INCORRECT_LOGIN.value, message.from_user.id])
        logging.info([f'Checking logins format {ms_login} - {success}', message.from_user.id])
    return wrapped


def check_delta_send_command(input_func):
    """
    Decorator for checking delta time between sending commands
    :param input_func: reference to async function
    """
    async def wrapped(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
        """
        Async function for checking delta between sending commands
        :return: call function or None
        """
        success = False
        data = await state.get_data()
        last_time = data.get("last_time", 0)
        remaining_time_second = (datetime.now() - datetime.fromtimestamp(last_time)).seconds
        if remaining_time_second >= settings.TG().command_pause_second:
            await state.update_data({"last_time": datetime.now().timestamp()})
            success = True
            await input_func(message, state)
        else:
            await message.reply(
                _messages.TgMessages.DELTA_FAIL.value.format(remaining_time_second=remaining_time_second)
            )
            logging.info([_messages.TgMessages.DELTA_FAIL.value, message.from_user.id])
        logging.info([
            f'Checking delta send message - {success}. '
            f'Remaining time - {remaining_time_second} second. '
            f'Command pause in settings - {settings.TG().command_pause_second} second. ',
            message.from_user.id
        ])
    return wrapped


@safe_try
async def handle_start(message: aiogram.types.Message,  state: aiogram.dispatcher.FSMContext) -> None:
    """Starting the bot and greeting"""
    ms_logins = db_actions.get_ms_logins_by_tg_id(tg_id=message.from_user.id)
    if ms_logins:
        response = _messages.TgMessages.START_KNOWN_USER.value.format(
                tg_username=message.from_user.username, ms_logins=ms_logins
        )
    else:
        response = _messages.TgMessages.START_UNKNOWN_USER.value
    await message.reply(response)
    logging.info([response, message.from_user.id])


@check_delta_send_command
@check_login_format
@safe_try
async def handle_del(message: aiogram.types.Message,  state: aiogram.dispatcher.FSMContext) -> None:
    """Add new user-subscriber by ms-login."""
    ms_login = message.get_args()
    if ms_login in db_actions.get_ms_logins_by_tg_id(tg_id=message.from_user.id):
        db_actions.delete_subscription(tg_id=message.from_user.id, ms_login=ms_login)
        response = _messages.TgMessages.DEL_SUCCESS.value.format(ms_login=ms_login)
    else:
        response = _messages.TgMessages.DEL_REJECT.value.format(ms_login=ms_login)
    await message.reply(response)
    logging.info([response, message.from_user.id])


@check_delta_send_command
@check_login_format
@safe_try
async def handle_add(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext) -> None:
    """Add new user-subscriber by ms-login."""
    ms_login = message.get_args()
    if ms_login in db_actions.get_ms_logins_by_tg_id(tg_id=message.from_user.id):
        response = _messages.TgMessages.ADD_REJECT.value.format(ms_login=ms_login)
    else:
        db_actions.add_subscription(tg_id=message.from_user.id, ms_login=ms_login)
        response = _messages.TgMessages.ADD_SUCCESS.value.format(ms_login=ms_login)
    await message.reply(response)
    logging.info([response, message.from_user.id])


async def handle_help(message: aiogram.types.Message) -> None:
    """Calling help by commands"""
    response = _messages.TgMessages.HELP_MSG.value
    await message.reply(response)
    logging.info([response, message.from_user.id])


async def handle_unknown(message: aiogram.types.Message) -> None:
    """A response to any unexpected message"""
    response = _messages.TgMessages.UNKNOWN_MESSAGE.value
    await message.reply(response)
    logging.info([response, message.from_user.id])
