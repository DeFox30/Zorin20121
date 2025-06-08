class ListMath:
    def __init__(self, lst=None):
        self.lst_math = []
        if lst:
            self.lst_math = [x for x in lst if type(x) in (int, float)]

    def _apply(self, other, op):
        return ListMath([op(x, other) for x in self.lst_math])

    def _apply_reverse(self, other, op):
        return ListMath([op(other, x) for x in self.lst_math])

    def _apply_inplace(self, other, op):
        self.lst_math = [op(x, other) for x in self.lst_math]
        return self

    def __add__(self, other):
        return self._apply(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self._apply_reverse(other, lambda x, y: x + y)

    def __iadd__(self, other):
        return self._apply_inplace(other, lambda x, y: x + y)

    def __sub__(self, other):
        return self._apply(other, lambda x, y: x - y)

    def __rsub__(self, other):
        return self._apply_reverse(other, lambda x, y: x - y)

    def __isub__(self, other):
        return self._apply_inplace(other, lambda x, y: x - y)

    def __mul__(self, other):
        return self._apply(other, lambda x, y: x * y)

    def __rmul__(self, other):
        return self._apply_reverse(other, lambda x, y: x * y)

    def __imul__(self, other):
        return self._apply_inplace(other, lambda x, y: x * y)

    def __truediv__(self, other):
        return self._apply(other, lambda x, y: x / y)

    def __rtruediv__(self, other):
        return self._apply_reverse(other, lambda x, y: x / y)

    def __itruediv__(self, other):
        return self._apply_inplace(other, lambda x, y: x / y)
