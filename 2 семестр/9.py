class WordString:
    def __init__(self, string=""):
        self.string = string
        self._words = string.split()

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, value):
        self._string = value
        self._words= value.split()

    def __len__(self):
        return len(self._words)

    def __call__(self, indx):
        return self._words[indx] if 0 <= indx < len(self._words) else ""

# Проверка
words = WordString("Python OOP")
print(len(words))
print(words(0))
words.string = "Java и Spring"
print(len(words))