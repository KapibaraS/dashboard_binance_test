import time
from asyncio import AbstractEventLoop

from motor.motor_asyncio import AsyncIOMotorClient


def get_timestamp():
    return int(time.time() * 1000)


def create_ws_url(is_combined=False):
    stream_url = 'wss://stream.binance.com:9443'
    if is_combined:
        stream_url += '/stream'
    else:
        stream_url += '/ws'

    return stream_url


def create_ws_message(method, pair, speed=1000):
    _id = get_timestamp()
    return {"method": f"{method}", "params": [f"{pair}@depth@{speed}ms"], "id": _id}


def mongo_conn_startup(dsn: str, db_name: str, loop: AbstractEventLoop):
    client = AsyncIOMotorClient(
       dsn, io_loop=loop
    )
    db_connection = client[db_name]
    return client, db_connection


def mongo_conn_shutdown(mongo_client: AsyncIOMotorClient) -> None:
    mongo_client.close()
