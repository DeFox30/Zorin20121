def find_expression(numbers, target, index=1, current_expression=None, current_value=None):
    if current_expression is None:
        current_expression = str(numbers[0])
    if current_value is None:
        current_value = numbers[0]

    # Если дошли до конца списка
    if index == len(numbers):
        if current_value == target:
            return current_expression + "=" + str(target)
        return None

    # Номер с +
    result = find_expression(numbers, target, index + 1,
                             current_expression + "+" + str(numbers[index]),
                             current_value + numbers[index])
    if result:
        return result

    # Номер с -
    result = find_expression(numbers, target, index + 1,
                             current_expression + "-" + str(numbers[index]),
                             current_value - numbers[index])
    if result:
        return result

    return None

# Чтение входных данных
data = input("N, X1...Xn, S: ").strip().split()
N = int(data[0])
numbers = list(map(int, data[1:N+1]))
S = int(data[N+1])

# Начальная точка рекурсии
result = find_expression(numbers, S)

# Запись результата в файл
with open('output.txt', 'w') as f:
    if result:
        f.write(result + '\n')
    else:
        f.write("no solution\n")
