import asyncio

import aiogram
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import settings
from ._message_handlers import handle_start, handle_del, handle_add, handle_help, handle_unknown

storage = RedisStorage2(
    host=settings.Redis().server,
    port=settings.Redis().port,
    db=settings.Redis().db_storage,
    pool_size=settings.Redis().storage_pool_size,
    prefix=settings.Redis().storage_prefix
)
oken = settings.TG().bot_token
bot = aiogram.Bot(token=settings.TG().bot_token, parse_mode='html')
loop = asyncio.get_event_loop()
dp = aiogram.Dispatcher(bot=bot, storage=storage, loop=loop)
dp.middleware.setup(LoggingMiddleware())

dp.register_message_handler(handle_start, commands=['start'])
dp.register_message_handler(handle_del, commands=['del'], state="*")
dp.register_message_handler(handle_add, commands=['add'], state="*")
dp.register_message_handler(handle_help, commands=['help'])
dp.register_message_handler(handle_unknown)
