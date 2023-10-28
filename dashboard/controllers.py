import aiohttp
import aiohttp_jinja2
import pandas as pd
from aiohttp import web, ClientSession

from dashboard.aggregate_orderbook import aggregate_levels
from dashboard.config import config

from logging import getLogger
log = getLogger(__name__)


REST_URL = config['REST_URL_BINANCE']
LEVELS_TO_SHOW = 10
PARAMS = {
        'symbol': 'BTCUSDT',
        'limit': 1000
    }


async def index(request):

    async with ClientSession() as session:
        async with session.get(REST_URL, params=PARAMS) as resp:
            if resp.status == 200:
                data = await resp.json()
                # TODO cpu-bound потеційно проблемне місце при зростанні глибини стакану
                bid_df = pd.DataFrame(data['bids'], columns=['price', 'quantity'], dtype=float)
                ask_df = pd.DataFrame(data['bids'], columns=['price', 'quantity'], dtype=float)
                bid_df = aggregate_levels(bid_df)
                ask_df = aggregate_levels(ask_df, side='asks')

    bid_df = bid_df.iloc[:LEVELS_TO_SHOW]
    ask_df = ask_df.iloc[:LEVELS_TO_SHOW]
    response = aiohttp_jinja2.render_template(
        'index.html',
        request,
        {
            'asks': ask_df.to_dict('records'),
            'bids': bid_df.to_dict('records'),
        }
    )
    return response


async def ws_order_book_update_depth(request):
    ws = web.WebSocketResponse()

    await ws.prepare(request)
    request.ws_connections.append(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                break
        elif msg.type == aiohttp.WSMsgType.ERROR:
            log.error(f'ws connection closed with exception {ws.exception()}')

    await ws.close()
    request.ws_connections.remove(ws)
    return ws