import queue
import threading
import time


class StopActiveObject(Exception):
    pass


class StopNoWaitActiveObject(Exception):
    pass


class ActiveObject(threading.Thread):
    def __init__(self, group=None, daemon=None, autostart=True, *args, **kwargs):
        super().__init__(target=self.executor, group=group, daemon=daemon, args=args, kwargs=kwargs)
        self.tasks = queue.SimpleQueue()
        if autostart:
            self.start()

    def executor(self, *args, **kwargs):
        while True:
            try:
                self.tasks.get()(*args, **kwargs)
            except StopNoWaitActiveObject:
                return
            except StopActiveObject:
                if self.tasks.empty():
                    return
                else:
                    self.stop()
            except Exception as e:
                print(type(e))
                print(e)

    def stop_no_wait(self):
        def _():
            raise StopNoWaitActiveObject()
        self.tasks.put(_)

    def stop(self):
        def _(*_, **__):
            raise StopActiveObject()
        self.tasks.put(_)
        self.join()

    def eat(self):
        self.tasks.put(lambda *, creature: print(f'{creature} eating'))

    def hunt(self):
        def _(*, creature):
            print(f'{creature} hunting')
            time.sleep(10)
            self.tasks.put(lambda *, creature: print(f'{creature} cooking'))
        self.tasks.put(_)

    def meditate(self):
        def _(*, creature):
            print(f'{creature} meditate')
            time.sleep(2)
        self.tasks.put(_)


def main():
    orc = ActiveObject(creature='Orc')
    orc.hunt()
    orc.eat()
    orc.stop()

    elven = ActiveObject(creature='Elven')
    elven.eat()
    elven.meditate()
    elven.meditate()
    elven.meditate()
    elven.meditate()
    elven.stop()


if __name__ == '__main__':
    main()
