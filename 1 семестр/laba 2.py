def safe(board, x, y, n):
    # Возможные движения верблюда
    verblud_moves = [
        (3, 1), (3, -1), (-3, 1), (-3, -1),
        (1, 3), (1, -3), (-1, 3), (-1, -3)
    ]
    for dx, dy in verblud_moves:
        # Проверка, не выходит ли клетка за пределы доски и находится ли она под угрозой
        if 0 <= x + dx < n and 0 <= y + dy < n and board[x + dx][y + dy] == 1:
            return False
    return True


def place_verblud(board, n, remaining, solutions, current_solution, start):
    if remaining == 0:
        # Сохраняем текущее решение, если все фигуры размещены
        solutions.add(tuple(sorted(current_solution)))
        return

    for i in range(start, n * n):
        x, y = divmod(i, n)
        if board[x][y] == 0 and safe(board, x, y, n):
            # Устанавка фигур на доску
            board[x][y] = 1
            current_solution.append((x, y))

            # Размещение оставшихся фигур
            place_verblud(board, n, remaining - 1, solutions, current_solution, i + 1)

            # Возвращение клетки в начальное состояние
            board[x][y] = 0
            current_solution.pop()


def threats(board, n):
    # Инициализация доски угроз
    threat_board = [['0'] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:  # Если на клетке стоит фигура
                threat_moves = [
                    (3, 1), (3, -1), (-3, 1), (-3, -1),
                    (1, 3), (1, -3), (-1, 3), (-1, -3)
                ]
                for dx, dy in threat_moves:
                    # Помечаем клетки, находящиеся под угрозой
                    if 0 <= i + dx < n and 0 <= j + dy < n:
                        threat_board[i + dx][j + dy] = '*'
    return threat_board


def print_board(board, n):
    threat_board = threats(board, n)
    for i in range(n):
        row = ''
        for j in range(n):
            if board[i][j] == 1:
                row += '# '  # Размещенная фигура
            elif threat_board[i][j] == '*':
                row += '* '  # Угроза
            else:
                row += '0 '  # Пустая клетка
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
            # Форматирование координат для записи в файл
            formatted_solution = ' '.join(f"({x},{y})" for x, y in solution)
            f.write(formatted_solution + '\n')  # Запись решения в файл

# Вывод доски и общее количество решений
print_board(board, n)
print("Общее количество уникальных решений:", len(solutions))
