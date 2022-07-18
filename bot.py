import asyncio
import logging

import database
import settings
from redis_pubsub import Subscriber
from telegram import dp
from telegram.utils import ms_problems_callback

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


async def shutdown():
    await Subscriber.close()
    logging.info('Redis subscriber stop - successful')
    bot_session = await dp.bot.get_session()
    await bot_session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.info('Bot stop - successful')


if __name__ == '__main__':
    logging.info("start bot")
    database.DBManager.initialize_db()
    logging.info('Database initialized - successful')
    loop = asyncio.get_event_loop()
    pubsub_task = loop.create_task(Subscriber.subscribe_to_channels(
        {settings.Redis().subscribe_key: ms_problems_callback})
    )
    logging.info('Redis subscriber start - successful')
    tg_polling_task = loop.create_task(dp.start_polling())
    logging.info('Bot start - successful')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('Keyboard Interrupt was gotten')
    finally:
        logging.info('Stop application begin')
        pubsub_task.cancel()
        tg_polling_task.cancel()
        loop.run_until_complete(shutdown())
        loop.close()
        database.DBManager.database.close()
        logging.info('Database connection close - successful')
        logging.info('Stop application end')
