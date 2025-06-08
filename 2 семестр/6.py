class Book:
    def __init__(self, title = "", author ="", pages = 0, year=0):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year

    def __setattr__(self, key, value):
        if key in ("title", "author"):
            if not isinstance(value, str):
                raise TypeError("Неверный тип данных")
        elif key in ("pages", "year"):
            if not isinstance(value, int):
                raise TypeError("Неверный тип данных")
        super().__setattr__(key, value)

book = Book("OOP", "JK", 123, 2022)