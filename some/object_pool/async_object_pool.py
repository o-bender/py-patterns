import asyncio
from asyncio import events


class AsyncObjectPoolThresholdExited(Exception):
    pass


class AsyncObjectPoolInstance:
    pass


class AsyncObjectPool:
    def __init__(self, threshold=10, loop=None, instance_builder=AsyncObjectPoolInstance):
        if loop is None:
            self._loop = events.get_event_loop()
        else:
            self._loop = loop

        self.available = []
        self.in_use = []
        self.threshold = threshold
        self.instance_builder = instance_builder

    async def acquire(self) -> AsyncObjectPoolInstance:
        while not self.available and len(self.in_use) >= self.threshold:
            getter = self._loop.create_future()
            try:
                await getter
            except:
                getter.cancel()
                raise

        return self.acquire_no_wait()

    def acquire_no_wait(self) -> AsyncObjectPoolInstance:
        if not self.available:
            if len(self.in_use) >= self.threshold:
                raise AsyncObjectPoolThresholdExited()

            self.available.append(self.instance_builder())

        instance = self.available.pop()
        self.in_use.append(instance)
        return instance

    def free(self, instance: AsyncObjectPoolInstance):
        i = self.in_use.index(instance)
        self.in_use.pop(i)
        self.available.append(instance)


async def run():
    pool = AsyncObjectPool(6)
    objects = await asyncio.gather(
        pool.acquire(),
        pool.acquire(),
        pool.acquire(),
        pool.acquire()
    )
    for p in objects:
        print(p)

    list(map(pool.free, objects))

    tasks = list(map(lambda _: asyncio.wait_for(pool.acquire(), timeout=1.0), range(5)))
    objects = await asyncio.gather(*tasks)
    print()
    for p in objects:
        print(p)

    tasks = list(map(lambda _: asyncio.wait_for(pool.acquire(), timeout=1.0), range(6)))
    objects = await asyncio.gather(*tasks)
    print()
    for p in objects:
        print(p)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())



