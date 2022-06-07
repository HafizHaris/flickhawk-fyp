class InMemoryItemStore(object):
    __ITEM_STORE = None

    @classmethod
    def pop_items(cls):
        items = cls.__ITEM_STORE or []
        cls.__ITEM_STORE = None
        return items

    @classmethod
    def add_item(cls, item):
        if not cls.__ITEM_STORE:
            cls.__ITEM_STORE = []
        cls.__ITEM_STORE.append(item)