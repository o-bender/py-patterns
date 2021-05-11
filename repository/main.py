import abc
import redis
import pickle
import copy


class AbstractCRUDRepository(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def create(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, item_id):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, item_id, value):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, item_id):
        raise NotImplementedError


class ListRepository(AbstractCRUDRepository):
    def __init__(self):
        super().__init__()
        self.data = []

    def create(self, value):
        value = copy.copy(value)
        value.id = len(self.data)
        self.data.append(value)
        return value.id

    def read(self, item_id):
        return self.data[item_id]

    def update(self, item_id, value):
        self.data[item_id] = copy.copy(value)

    def delete(self, item_id):
        self.data.pop(item_id)


class RedisRepository(AbstractCRUDRepository):
    def __init__(self, dsn=None):
        super().__init__()
        self.engine = redis.Redis(dsn)

    def create(self, value):
        value = copy.copy(value)
        value.id = id(value)
        self.engine.append(id(value), pickle.dumps(value))
        return id(value)

    def read(self, item_id):
        byte_string = self.engine.get(item_id)
        if byte_string:
            return pickle.loads(byte_string)

    def delete(self, item_id):
        self.engine.delete(item_id)

    def update(self, item_id, value):
        if item_id == id(value):
            self.create(value)


class User:
    id: int = 0
    name: str = None
    fullname: str = None
    password: str = None

    def __init__(self, name, fullname, password):
        self.id = 0
        self.name = name
        self.fullname = fullname
        self.password = password

    def __str__(self):
        return f'{self.id} {self.fullname}'


if __name__ == '__main__':
    u = User('Льюис', 'Льюис Тэрин Теламон', '123456')
    u2 = User('Морейн', 'Морейн Дамодред', '123456')
    repo1 = ListRepository()
    u_id = repo1.create(u)
    u2_id = repo1.create(u2)
    print(u)
    print(u_id, repo1.read(u_id))
    print(u2)
    print(u2_id, repo1.read(u2_id))

    repo2 = RedisRepository()
    u_id = repo2.create(u)
    print(u)
    print(u_id, repo2.read(u_id))

    u_id = repo2.create(u2)
    print(u2)
    print(u_id, repo2.read(u_id))