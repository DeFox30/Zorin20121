from itertools import combinations

def unique_subsets(elements):
    # Удаляем дубликаты, используя множество
    unique_elements = list(set(elements))
    subsets = []

    # Генерируем подмножества различной длины
    for r in range(1, len(unique_elements) + 1):
        for combo in combinations(unique_elements, r):
            subsets.append(set(combo))  # Добавляем каждую комбинацию как множество

    return subsets, len(subsets)

# Ввод данных
input_list = input("Элементы списка: ").split()

# Получение результатов
subsets, count = unique_subsets(input_list)

# Печать результатов
print("Подмножества:", subsets)
print("Количество подмножеств:", count)