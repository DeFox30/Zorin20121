def skobki(n):
    def posledovatelnost(posl, open, close):
        if len(posl) == 2*n:
            res.append(posl)
            return
        if open<n:
            posledovatelnost(posl+"(", open+1, close)
        if close<open:
            posledovatelnost(posl+")", open, close+1)

    res = []
    posledovatelnost("", 0, 0)
    return res


print(skobki(1))