class ObjectPoolThresholdExited(Exception):
    pass


class ObjectPoolInstance:
    pass


class ObjectPool:
    def __init__(self, threshold=10, instance_builder=ObjectPoolInstance):
        self.available = []
        self.in_use = []
        self.threshold = threshold
        self.instance_builder = instance_builder

    def acquire(self) -> ObjectPoolInstance:
        if not self.available:
            if len(self.in_use) >= self.threshold:
                raise ObjectPoolThresholdExited()

            self.available.append(self.instance_builder())

        instance = self.available.pop()
        self.in_use.append(instance)
        return instance

    def free(self, instance: ObjectPoolInstance):
        i = self.in_use.index(instance)
        self.in_use.pop(i)
        self.available.append(instance)


if __name__ == '__main__':
    pool = ObjectPool(6)
    o1 = pool.acquire()
    o2 = pool.acquire()
    o3 = pool.acquire()
    o4 = pool.acquire()
    for p in (o1, o2, o3, o4):
        print(p)
    pool.free(o2)
    pool.free(o4)
    pool.free(o1)
    pool.free(o3)

    o1 = pool.acquire()
    o2 = pool.acquire()
    o3 = pool.acquire()
    o4 = pool.acquire()
    o5 = pool.acquire()
    print()
    for p in (o1, o2, o3, o4, o5):
        print(p)

    o1 = pool.acquire()
    o2 = pool.acquire()
    o3 = pool.acquire()
    o4 = pool.acquire()
    o5 = pool.acquire()
    o6 = pool.acquire()
    print()
    for p in (o1, o2, o3, o4, o5, o6):
        print(p)


