from aiohttp import web
from functools import wraps


async def db_handler(app, handler):
    @web.middleware
    @wraps(handler)
    async def middleware(request):
        request.db = app['mongodb_connection']
        request.db_cli = app['mongodb_client']
        response = await handler(request)
        return response
    return middleware