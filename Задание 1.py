from itertools import combinations

# Вводим данные
n = int(input())  # количество элементов в списке
lst = list(map(int, input().split()))  # сам список
c = int(input())  # целевое значение

# Ищем комбинации из 4 чисел
closest_combination = None
closest_sum = float('inf')

for comb in combinations(lst, 4):
    comb_sum = sum(comb)
    # Проверяем, если сумма комбинации ближе к цели
    if abs(comb_sum - c) < abs(closest_sum - c):
        closest_combination = comb
        closest_sum = comb_sum

# Выводим результат
print(list(closest_combination))
print(closest_sum)