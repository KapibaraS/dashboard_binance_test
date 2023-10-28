import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp import web

from dashboard.config import TEMPLATE_DIR
from dashboard.rbmq import listener
from dashboard.routes import setup_routes
from dashboard.middlewares import connections_handler


async def create_app(config: dict) -> web.Application:
    app = web.Application(
        debug=config['debug'],
        middlewares=[
            normalize_path_middleware(),
            connections_handler,
        ]
    )
    app['config'] = config
    app['ws_connections'] = []
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(TEMPLATE_DIR)
    )
    setup_routes(app)

    loop = asyncio.get_event_loop()
    app['websocket_task'] = loop.create_task(listener(app))

    return app
