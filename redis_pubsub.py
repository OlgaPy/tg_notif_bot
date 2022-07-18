import typing

import aioredis

import settings


class Subscriber:
    """Class for rule publisher-subscriber from redis"""

    pubsub: typing.Optional[aioredis.client.PubSub] = None

    @classmethod
    async def subscribe_to_channels(cls, channels: typing.Dict[str, typing.Callable]) -> None:
        """
        Start redis worker
        """

        cls.pubsub = aioredis.client.PubSub(
            connection_pool=aioredis.ConnectionPool.from_url(f'redis://{settings.Redis().server}')
        )
        await cls.pubsub.subscribe(**channels)
        await cls.pubsub.run()

    @classmethod
    async def close(cls):
        if cls.pubsub:
            await cls.pubsub.unsubscribe()
            await cls.pubsub.connection_pool.disconnect()
