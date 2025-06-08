class NewList:
    def __init__(self, lst=None):
        self.lst = lst if lst is not None else []

    def __sub__(self, other):
        if isinstance(other, (list, NewList)):
            other_list = other.lst if isinstance(other, NewList) else other
            other_counts = {}
            for item in other_list:
                key = (item, type(item))
                other_counts[key] = other_counts.get(key, 0) + 1

                new_list = []
                temp_counts = other_counts.copy()

                for item in self.lst:
                    key = (item, type(item))
                    if key in temp_counts and temp_counts[key] > 0:
                        temp_counts[key] -= 1
                    else:
                        new_list.append(item)
        return NewList(new_list)

    def __rsub__(self, other):
        if isinstance(other, list):
            return NewList(other) - self

    def get_list(self):
        return self.lst


# Proverka
lst = NewList()
lst1 = NewList([0, 1, -3.4, "abc", True])
lst2 = NewList([1, 0, True])
assert lst1.get_list() == [0, 1, -3.4, "abc", True] and lst.get_list() == []
res1 = lst1 - lst2
res2 = lst1 - [0, True]
res3 = [1, 2, 3, 4.5] - lst2
lst1 -= lst2
assert res1.get_list() == [-3.4, "abc"]
assert res2.get_list() == [1, -3.4, "abc"]
assert res3.get_list() == [2, 3, 4.5]
assert lst1.get_list() == [-3.4, "abc"]
lst_1 = NewList([1, 0, True, False, 5.0, True, 1, True, -7.87])
