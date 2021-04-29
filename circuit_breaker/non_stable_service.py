import asyncio
from aiohttp import web
from random import random


async def non_stable_service(request):
    if random() > 0.2:
        await asyncio.sleep(10)
    return web.Response(text="success response")

if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/{id}', non_stable_service),
    ])
    web.run_app(app)
