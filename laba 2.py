def safe(board, x, y, N):
    # Находиться ли клетка под угрозой
    verblud_moves = [
        (3, 1), (3, -1), (-3, 1), (-3, -1),
        (1, 3), (1, -3), (-1, 3), (-1, -3)
    ]

    for dx, dy in verblud_moves:
        if 0 <= x + dx < N and 0 <= y + dy < N and board[x + dx][y + dy] == 1:
            return False
    return True

def place_verblud(board, N, remaining, solutions, current_solution):
    if remaining == 0:
        solutions.append(current_solution.copy())
        return

    for i in range(N):
        for j in range(N):
            if board[i][j] == 0 and safe(board, i, j, N):
                # Установить верблюда
                board[i][j] = 1
                current_solution.append((i, j))

                # Расстановка оставшихся верблюдов
                place_verblud(board, N, remaining - 1, solutions, current_solution)

                # Удалить верблюда
                board[i][j] = 0
                current_solution.pop()

def threats(board, N):
    # Доска для угроз
    threat_board = [['0'] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if board[i][j] == 1:  # Если на доске есть фигура
                threat_moves = [
                    (3, 1), (3, -1), (-3, 1), (-3, -1),
                    (1, 3), (1, -3), (-1, 3), (-1, -3)
                ]
                for dx, dy in threat_moves:
                    if 0 <= i + dx < N and 0 <= j + dy < N:
                        threat_board[i + dx][j + dy] = '*'

    return threat_board

def print_board(board, N):
    threat_board = threats(board, N)

    for i in range(N):
        row = ''
        for j in range(N):
            if board[i][j] == 1:
                row += '# '
            elif threat_board[i][j] == '*':
                row += '* '
            else:
                row += '0 '
        print(row.strip())

# Ввод данных
N, L, K = map(int, input("N(размер доски), L(фигуры для размещения), K(фигуры на доске): ").split())

board = [[0] * N for _ in range(N)]
positions = []

for _ in range(K):
    x, y = map(int, input("Координаты фигуры: ").split())
    board[x][y] = 1
    positions.append((x, y))

solutions = []
place_verblud(board, N, L, solutions, positions)

# Вывод всех решений
if not solutions:
    print("no solutions")
else:
    for solution in solutions:
        print(', '.join(f"({x},{y})" for x, y in solution))

# Вывод доски
print_board(board, N)
print("Общее количество решений:", len(solutions))