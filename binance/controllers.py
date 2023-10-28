import json

import aiohttp

from binance.rbmq import publish_message
from binance.utils import create_ws_url, create_ws_message


async def callback(msg, app):
    db = app['mongodb_connection']
    await db.orderBooks.insert_one(json.loads(msg))
    await publish_message(msg)


async def websocket(app):
    stream_url = create_ws_url()

    async with aiohttp.ClientSession() as session:
        ws = await session.ws_connect(stream_url)
        await ws.send_json(create_ws_message("SUBSCRIBE", "btcusdt"))

        async for msg in ws:

            if msg.type == aiohttp.WSMsgType.TEXT:
                await callback(msg.data, app)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        await ws.send_json(create_ws_message("UNSUBSCRIBE", "btcusdt",))
