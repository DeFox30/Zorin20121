from random import choice

class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0

class TicTacToe:
    FREE_CELL = 0  # Свободная клетка игрока
    HUMAN_X = 1  # Крестик (человек)
    COMPUTER_0 = 2  # Нолик (компьютер)

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for __ in range(3))

    def __getitem__(self, indices):
        i, j = indices
        if not (isinstance(i, int) and isinstance(j, int)) or not (0 <= i < 3 and 0 <= j < 3):
            raise IndexError("Некорректно указаны индексы")
        return self.pole[i][j].value

    def __setitem__(self, indices, value):
        i, j = indices
        if not (isinstance(i, int) and isinstance(j, int)) or not (0 <= i < 3 and 0 <= j < 3):
            raise IndexError("Некорректно указаны индексы")
        if value not in (self.FREE_CELL, self.HUMAN_X, self.COMPUTER_0):
            raise ValueError("Некорректное значение")
        self.pole[i][j].value = value

    def init(self):
        for row in self.pole:
            for cell in row:
                cell.value = self.FREE_CELL

    def show(self):
        for row in self.pole:
            print(' '.join(str(cell.value) for cell in row))
        print()

    def human_go(self):
        while True:
            try:
                coords = input("Координаты i j: ").split()
                i, j = map(int, coords)
                if self[i,j] == self.FREE_CELL:
                    self[i,j] = self.HUMAN_X
                    break
                print("Клетка занята")
            except (ValueError, IndexError):
                print("Некорректный ввод")

    def computer_go(self):
        free = [(i,j) for i in range(3) for j in range(3) if self[i,j] == self.FREE_CELL]
        if free:
            i, j = choice(free)
            self[i,j] = self.COMPUTER_0

    @property
    def is_human_win(self):
        return self._check_win(self.HUMAN_X)

    @property
    def is_computer_win(self):
        return self._check_win(self.COMPUTER_0)

    @property
    def is_draw(self):
        return (not self.is_human_win and not self.is_computer_win and all(cell.value != self.FREE_CELL for row in self.pole for cell in row))

    def __bool__(self):
        return not (self.is_human_win or self.is_computer_win or self.is_draw)

    def _chek_win(self, player):
        for row in self.pole:
            if all(cell.value == player for cell in row):
                return True
        for col in range(3):
            if all(self.pole[row][col].value == player for row in range(3)):
                return True
        if all(self.pole[i][i].value == player for i in range(3)):
            return True
        if all(self.pole[i][2-i].value == player for i in range(3)):
            return True
        return False