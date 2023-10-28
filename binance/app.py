import asyncio

from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware

from binance.controllers import websocket
from binance.middlewares import db_handler
from binance.routes import setup_routes
from binance.utils import mongo_conn_shutdown, mongo_conn_startup


async def init_db(app: web.Application) -> None:
    dsn = app['config']['mongodb']['dsn']
    db_name = app['config']['mongodb']['db_name']

    mongodb_client, mongodb_connection = mongo_conn_startup(
        dsn, db_name, app.loop,
    )

    app['mongodb_client'] = mongodb_client
    app['mongodb_connection'] = mongodb_connection
    # await create_index(mongodb_connection)


async def cleanup_db(app: web.Application) -> None:
    mongo_conn_shutdown(app['mongodb_client'])


async def create_app(config: dict) -> web.Application:
    app = web.Application(
        debug=config['debug'],
        middlewares=[
            normalize_path_middleware(),
            db_handler,
        ]
    )
    app['config'] = config
    setup_routes(app)
    loop = asyncio.get_event_loop()
    app['websocket_task'] = loop.create_task(websocket(app))
    app.on_startup.append(init_db)
    app.on_cleanup.append(cleanup_db)
    return app
