from aiohttp import web
from functools import wraps


async def connections_handler(app, handler):
    @web.middleware
    @wraps(handler)
    async def middleware(request):
        request.ws_connections = app['ws_connections']
        response = await handler(request)
        return response
    return middleware
