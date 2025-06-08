class Ingredient:
    def __init__(self, name, volume, measure):
        self.name = name
        self.volume = volume
        self.measure = measure

    def __str__(self):
        return f"{self.name}: {self.volume}, {self.measure}"


class Recipe:
    def __init__(self, *ingredients):
        self._ingredients = list(ingredients)

    def add_ingredient(self, ing):
        self._ingredients.append(ing)

    def remove_ingredient(self, ing):
        if ing in self._ingredients:
            self._ingredients.remove(ing)

    def get_ingredients(self):
        return tuple(self._ingredients)

    def __len__(self):
        return len(self._ingredients)
