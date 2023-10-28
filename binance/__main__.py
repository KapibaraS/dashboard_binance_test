import asyncio

from aiohttp import web

from binance.app import create_app
from binance.config import config

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


if __name__ == '__main__':
    app = create_app(config)
    web.run_app(app, port=8000)
