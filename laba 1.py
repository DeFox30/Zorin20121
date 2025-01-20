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

    # текущий номер с +
    result = find_expression(numbers, target, index + 1,
                             current_expression + "+" + str(numbers[index]),
                             current_value + numbers[index])
    if result:
        return result

    # текущий номер с -
    result = find_expression(numbers, target, index + 1,
                             current_expression + "-" + str(numbers[index]),
                             current_value - numbers[index])
    if result:
        return result

    return None

data = input().strip().split()
N = int(data[0])
numbers = list(map(int, data[1:N+1]))
S = int(data[N+1])

result = find_expression(numbers, S)

if result:
    print(result)
else:
    print("no solution")
