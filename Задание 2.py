def func(a):
    rom_num = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    res = 0
    b = 0

    for i in range(len(a) - 1, -1, -1):
        val = rom_num[a[i]]
        if val < b:
            res -= val
        else:
            res += val
        b = val

    return res

print(func("MDXI"))