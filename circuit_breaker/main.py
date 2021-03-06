from asyncio import Queue
from datetime import timedelta
from http.client import HTTPSConnection
from circuit_breaker import CircuitBreaker, States
from time import sleep
import asyncio
from aiohttp import web, ClientSession, ClientTimeout
from asyncio.exceptions import TimeoutError
from datetime import datetime
from random import random
from collections import ChainMap


async def get(endpoint, timeout):
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        print(f'GET {endpoint}')
        async with session.get(endpoint) as resp:
            print(f'{endpoint} {resp.status}')
            if resp.ok:
                return await resp.text()


async def run():
    tasks = []
    for i in range(20):
        task = asyncio.create_task(cb.attempt_request(
            endpoint=f'http://localhost:8080/{i}'
        ))
        tasks.append(task)
        await asyncio.sleep(random())
    responses = await asyncio.gather(*tasks)
    for r in responses:
        print(r if isinstance(r, str) else r.__repr__())


if __name__ == '__main__':
    cb = CircuitBreaker(
        service=get,
        timeout=1,
        retry_timeout=timedelta(seconds=5),
        failure_threshold=4,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
