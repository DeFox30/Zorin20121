class WordString:
    def __init__(self, string=""):
        self._string = string

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, value):
        self._string = value

    def __len__(self):
        return len(self._string.split())

    def __call__(self, indx):
        words = self._string.split()
        return words[indx] if 0 <= indx < len(words) else ''
