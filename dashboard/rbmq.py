import asyncio
from asyncio import get_event_loop

from aio_pika import connect_robust

from dashboard.config import config

RMQ_CONN_STR = config['RMQ_CONN_STR']
RMQ_CHANNEL_NAME = config['RMQ_CHANNEL_NAME']


class Consumer:
    def __init__(self, ws_connections):
        self.ws_connections = ws_connections

    async def process_message(self, message):
        async with message.process():
            message.body.decode()
            await asyncio.gather(
                *(ws.send_json(message.body.decode()) for ws in self.ws_connections)
            )


async def listener(app):
    loop = get_event_loop()
    connection = await connect_robust(RMQ_CONN_STR, loop=loop)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(RMQ_CHANNEL_NAME, auto_delete=False)

    c = Consumer(app['ws_connections'])
    await queue.consume(callback=c.process_message)
    return connection
