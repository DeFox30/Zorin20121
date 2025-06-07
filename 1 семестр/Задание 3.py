def unique_permutations(nums):
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])  # Добавляем копию текущей перестановки
            return

        seen = set()  # Отслеживание уже использованных чисел
        for i in range(start, len(nums)):
            if nums[i] in seen:
                continue
            seen.add(nums[i])
            nums[start], nums[i] = nums[i], nums[start]  # Меняем местами
            backtrack(start + 1)  # Рекурсивный вызов
            nums[start], nums[i] = nums[i], nums[start]  # Возврат на предыдущий уровень

    result = []
    nums.sort()  # Сортировка для поиска дубликатов
    backtrack(0)
    return result


# Ввод данных с клавиатуры
input_data = input("Список чисел: ").split()

# Получение результата
output = unique_permutations(input_data)

print(output)
