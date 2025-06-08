from abc import abstractmethod


class Box:
    @abstractmethod
    def add(self, items):
        pass

    @abstractmethod
    def empty(self):
        pass

    @abstractmethod
    def count(self):
        pass


class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ListBox(Box):
    def __init__(self, items=None):
        if items is None:
            self.items = []
        else:
            self.items = items

    def add(self, items=None):
        for item in items:
            self.items.append(item)

    def empty(self):
        buf = self.items
        self.items = None
        return buf


class DictBox(Box):
    def __init__(self, items=None):
        if items in None:
            self.items = {}
        else:
            self.items = items

    def add(self, items):
        for item in items:
            if item.name not in self.items:
                self.items[item.name] = [item.value]
            else:
                self.items[item.name] += [item.value]

    def empty(self):
        buf = list()
        for name, value in self.items():
            buf.append(Item(name, value))
        self.items = None
        return buf

    def count(self):
        return len(self.items.names())


def repack(*args):
    collections = list(chain(*[box.empty() for box in boxes]))
    count = len(collections)//len(boxes)
    for box in boxes:
        box.add