def max_robbery(n, banks):
    if n == 0:
        return 0, []
    elif n == 1:
        return banks[0][1], [(banks[0][0], 1)]

    # Хранение максимальной суммы
    dp = [0] * n
    dp[0] = banks[0][1]
    dp[1] = max(banks[0][1], banks[1][1])

    # Отслеживание выбранных банков
    selected_banks = [[] for _ in range(n)]
    selected_banks[0] = [(banks[0][0], 1)]

    if banks[0][1] >= banks[1][1]:
        selected_banks[1] = selected_banks[0]
    else:
        selected_banks[1] = [(banks[1][0], 2)]

    for i in range(2, n):
        if dp[i - 1] > dp[i - 2] + banks[i][1]:
            dp[i] = dp[i - 1]
            selected_banks[i] = selected_banks[i - 1]
        else:
            dp[i] = dp[i - 2] + banks[i][1]
            selected_banks[i] = selected_banks[i - 2] + [(banks[i][0], i + 1)]

    return dp[n - 1], selected_banks[n - 1]


# Ввод данных
n = int(input("количество банков: "))
banks = []

for _ in range(n):
    bank_info = input("название банка и сумма: ").split()
    bank_name = bank_info[0]
    bank_amount = int(bank_info[1])
    banks.append((bank_name, bank_amount))

# Получение результата
max_sum, selected_banks = max_robbery(n, banks)

# Вывод результата
print([max_sum] + selected_banks)