from queue import Queue
import threading


class Stop(Exception):
    pass


class EventSourcingList:
    def __init__(self):
        self.data = []
        self.event_queue = Queue()
        self.thread = threading.Thread(target=self.execute)
        self.thread.start()

    def append(self, value):
        self.event_queue.put(value)

    def get_all(self):
        return self.data

    def get(self, item_id: int):
        return self.data[item_id]

    def close(self):
        self.append(Stop())
        self.thread.join()

    def execute(self):
        while True:
            try:
                val = self.event_queue.get()
                if isinstance(val, Exception):
                    raise val
                self.data.append(val)
            except Stop:
                break
            except Exception as e:
                print(e)
