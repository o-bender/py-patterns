import asyncio
from aiohttp import web, ClientSession, ClientTimeout
from asyncio.exceptions import TimeoutError
from datetime import datetime
from random import random
from collections import ChainMap

ENDPOINTS = [
    'http://localhost:8080/card-service',
    'http://localhost:8080/card-operations-log',
    'http://localhost:8080/card-advert-service',
]


async def get(endpoint, params):
    async with ClientSession(timeout=ClientTimeout(total=4)) as session:
        try:
            async with session.get(endpoint, params=params) as resp:
                print(f'{endpoint} {resp.status}')
                if resp.ok:
                    return await resp.json()
        except TimeoutError:
            print(f'{endpoint} TimeoutError')
            return {}


async def aggregator_handler(request):
    tasks = []

    card_id = request.query.get('card_id')
    if card_id:
        for endpoint in ENDPOINTS:
            task = asyncio.ensure_future(get(endpoint, params={'card_id': card_id}))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return web.json_response(dict(ChainMap(*responses)))

    return web.json_response({'error': 'card_id required'}, status=400)


async def card_service_handler(request):
    card_id = request.query.get('card_id')
    return web.json_response({'card': {
        'id': card_id,
        'card': '1232343',
        'card_holder': 'Льюс Тэрин Тэламон',
        'cost': 100000
    }})


async def card_operations_log_handler(request):
    card_id = request.query.get('card_id')
    print(f'SELECT date, cost, currency FROM card_operations WITH card_id = {card_id}')
    await asyncio.sleep(3)
    return web.json_response({'transactions_log': [
        {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'cost': '1000',
            'currency': 'RUB',
        },
        {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'cost': '2000',
            'currency': 'RUB',
        },
        {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'cost': '3000',
            'currency': 'RUB',
        }
    ]})


async def card_advert_service_handler(request):
    timeout = int(random() * 10)
    print(f'ADVERT SERVICE timeout {timeout}')
    await asyncio.sleep(timeout)
    return web.json_response({
        'advert': 'best advert',
    })

app = web.Application()
app.add_routes([
    web.get('/', aggregator_handler),
    web.get('/card-service', card_service_handler),
    web.get('/card-operations-log', card_operations_log_handler),
    web.get('/card-advert-service', card_advert_service_handler),
])


if __name__ == '__main__':
    web.run_app(app)
