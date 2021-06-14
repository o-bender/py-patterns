import time
from engine import EventSourcingList


class GetItemQuery:
    def __init__(self, engine: EventSourcingList):
        self.engine = engine

    def execute(self, item_id: int):
        return self.engine.get(item_id)


class GetAllItemsQuery:
    def __init__(self, engine: EventSourcingList):
        self.engine = engine

    def execute(self):
        return self.engine.get_all()


class InsertItemCommand:
    def __init__(self, engine: EventSourcingList):
        self.engine = engine

    def execute(self, item):
        return self.engine.append(item)


def main():
    el = EventSourcingList()

    get_all_query = GetAllItemsQuery(el)
    get_item_query = GetItemQuery(el)
    insert_item_cmd = InsertItemCommand(el)

    print(
        list(map(
            insert_item_cmd.execute,
            ['hello', 'python', 'test', 'string', 'C', 'C++', 'JavaScript']
        ))
    )
    time.sleep(0.1)

    print(get_all_query.execute())
    print(
        get_item_query.execute(4),
        get_item_query.execute(5),
        get_item_query.execute(6),
    )

    el.close()


if __name__ == '__main__':
    main()
