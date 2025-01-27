def group_strings(strings):
    # Словарь для хранения групп
    grouped = {}

    for string in strings:
        # Сортируем буквы в строке для создания ключа
        sorted_string = ''.join(sorted(string))
        key = (sorted_string, len(string))  # Ключ состоит из отсортированной строки и длины

        if key not in grouped:
            grouped[key] = []  # Создаем новый список, если ключа нет
        grouped[key].append(string)  # Добавляем строку в группу

    # Возвращаем сгруппированные строки в виде списка
    return list(grouped.values())

# Ввод данных с клавиатуры
input_data = input("Строки: ").split()

# Получение результата
output = group_strings(input_data)

print(output)