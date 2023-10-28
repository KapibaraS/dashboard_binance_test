import json
from asyncio import get_event_loop

from aio_pika import connect_robust, Message

from binance.config import config
from binance.utils import get_timestamp

RMQ_CONN_STR = config['RMQ_CONN_STR']
RMQ_CHANNEL_NAME = config['RMQ_CHANNEL_NAME']


async def publish_message(message):
    """ Add message to RMQ """
    uid = get_timestamp()
    msg = {'id': str(uid), 'msg': message}
    connection = await connect_robust(RMQ_CONN_STR, loop=get_event_loop(), timeout=15)

    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            Message(
                body=json.dumps(msg).encode()
            ),
            routing_key=RMQ_CHANNEL_NAME
        )