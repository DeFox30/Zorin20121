class NewList:
    def __init__(self, lst=None):
        self._lst = lst[:] if lst is not None else []

    def get_list(self):
        return self._lst

    def __sub__(self, other):
        other_list = other._lst if isinstance(other, NewList) else list(other)
        result = self._lst[:]
        for item in other_list:
            if item in result:
                result.remove(item)
        return NewList(result)

    def __rsub__(self, other):
        other_list = other._lst if isinstance(other, NewList) else list(other)
        result = other_list[:]
        for item in self._lst:
            if item in result:
                result.remove(item)
        return NewList(result)

    def __isub__(self, other):
        other_list = other._lst if isinstance(other, NewList) else list(other)
        for item in other_list:
            if item in self._lst:
                self._lst.remove(item)
        return self
