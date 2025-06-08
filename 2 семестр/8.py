class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f"Книга: {self.title}; {self.author}; {self.pages}"

lst_in = ("Python", "JK", "1024")
book = Book(*lst_in)
print(book)

