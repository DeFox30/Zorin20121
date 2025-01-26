def analyze_lists(list1, list2):
    # Преобразуем списки в множества
    set1 = set(list1)
    set2 = set(list2)

    # 1) Элементы, присутствующие в обоих списках
    common_elements = set1 & set2

    # 2) Элементы, присутствующие только в одном списке
    unique_elements = set1 ^  set2

    # 3) Оставшиеся элементы в list1 после извлечения элементов из list2
    remaining_in_list1 = set1 - set2

    # 4) Оставшиеся элементы в list2 после извлечения элементов из list1
    remaining_in_list2 = set2 - set1

    return (
        len(common_elements),
        len(unique_elements),
        len(remaining_in_list1),
        len(remaining_in_list2),
        list(common_elements),  # Список общих элементов
        list(unique_elements),  # Список уникальных элементов
        list(remaining_in_list1),  # Список оставшихся элементов в list1
        list(remaining_in_list2)  # Список оставшихся элементов в list2
    )


# Ввод данных
list1_input = input("элементы первого списка: ")
list2_input = input("элементы второго списка: ")

# Преобразование в списки
list1 = list(map(int, list1_input.split()))
list2 = list(map(int, list2_input.split()))

# Вызов функции
results = analyze_lists(list1, list2)

# Печать результатов
print(f"1) {results[0]} элементов: {results[4]}")
print(f"2) {results[1]} элементов: {results[5]}")
print(f"3) {results[2]} элементов: {results[6]}")
print(f"4) {results[3]} элементов: {results[7]}")
