def safe(board, x, y, n):
    # Проверка, находится ли клетка под угрозой
    verblud_moves = [
        (3, 1), (3, -1), (-3, 1), (-3, -1),
        (1, 3), (1, -3), (-1, 3), (-1, -3)
    ]
    for dx, dy in verblud_moves:
        if 0 <= x + dx < n and 0 <= y + dy < n and board[x + dx][y + dy] == 1:
            return False
    return True


def place_verblud(board, n, remaining, solutions, current_solution, start):
    # Если все верблюды размещены, сохранить текущее решение
    if remaining == 0:
        solutions.add(tuple(sorted(current_solution)))
        return

    for i in range(start, n * n):
        x, y = divmod(i, n)
        if board[x][y] == 0 and safe(board, x, y, n):
            # Установить верблюда
            board[x][y] = 1
            current_solution.append((x, y))

            # Рекурсивно разместить оставшихся верблюдов
            place_verblud(board, n, remaining - 1, solutions, current_solution, i + 1)

            # Удалить верблюда
            board[x][y] = 0
            current_solution.pop()


def threats(board, n):
    # Генерация доски с угрозами
    threat_board = [['0'] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                threat_moves = [
                    (3, 1), (3, -1), (-3, 1), (-3, -1),
                    (1, 3), (1, -3), (-1, 3), (-1, -3)
                ]
                for dx, dy in threat_moves:
                    if 0 <= i + dx < n and 0 <= j + dy < n:
                        threat_board[i + dx][j + dy] = '*'
    return threat_board


def print_board(board, n):
    # Вывод доски
    threat_board = threats(board, n)
    for i in range(n):
        row = ''
        for j in range(n):
            if board[i][j] == 1:
                row += '# '
            elif threat_board[i][j] == '*':
                row += '* '
            else:
                row += '0 '
        print(row.strip())


# Ввод данных
n, l, k = map(int, input("Введите N (размер доски), L (фигуры для размещения), K (фигуры на доске): ").split())

# Инициализация доски
board = [[0] * n for _ in range(n)]
positions = []

# Размещение начальных фигур
for _ in range(k):
    x, y = map(int, input("Введите координаты фигуры: ").split())
    board[x][y] = 1
    positions.append((x, y))

# Поиск решений
solutions = set()
place_verblud(board, n, l, solutions, positions, 0)

# Запись решений в файл
with open('output2.txt', 'w') as f:
    if not solutions:
        f.write("no solutions\n")
    else:
        for solution in solutions:
            f.write(', '.join(f"({x},{y})" for x, y in solution) + '\n')

# Вывод доски
print_board(board, n)
print("Общее количество уникальных решений:", len(solutions))
