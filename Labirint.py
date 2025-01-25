def labirint(n,m):
    if n == 1 or m == 1:
        return 1
    return labirint(n-1,m) + labirint(n, m - 1)


print(labirint(n = 3, m = 3))
