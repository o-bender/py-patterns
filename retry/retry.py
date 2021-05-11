from functools import wraps
import time
from http import client
import socket


def retry(attempts_count: int, delay: float, exceptions=(Exception,)):
    def _(fn):
        @wraps(fn)
        def __(*args, **kwargs):
            for attempt in range(attempts_count):
                try:
                    print(f'Attempt {attempt}')
                    return fn(*args, **kwargs)
                except exceptions as e:
                    print(type(e))
                    if attempt < attempts_count:
                        print('Sleep...')
                        time.sleep(delay)
                    else:
                        raise e
        return __
    return _


@retry(3, 1, exceptions=(socket.timeout, Exception))
def get():
    conn = client.HTTPSConnection('www.some.ru', timeout=3)
    try:
        conn.request('GET', '/')
    finally:
        conn.close()


def main():
    get()


if __name__ == '__main__':
    main()
