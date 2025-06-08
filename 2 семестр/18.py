import sys

class ShopItem:
    def __init__(self, name, weight, price):
        self.name = name
        self.weight = weight
        self.price = price

    def __hash__(self):
        return hash((self.name.lower(), self.weight, self.price))

    def __eq__(self, other):
        if not isinstance(other, ShopItem):
            return False
        return hash(self) == hash(other)

shop_items = {}

for line in lst_in:
    parts = line.split(':')
    for i in range(len(parts) - 1):
        name = parts[i].strip().split()
        next_values = parts[i + 1].strip().split()

        if name and name[-1].replace('.', '', 1).isdigit():
            name = name[:-1]
        item_name = ' '.join(name)

        weight = float(next_values[0])
        price = float(next_values[1])

        item = ShopItem(item_name, weight, price)

        if item in shop_items:
            shop_items[item][1] += 1
        else:
            shop_items[item] = [item, 1]
