class CustomList(list):
    def __add__(self, other: list):
        result = CustomList(other[:])
        delta_len = len(self) - len(result)
        if delta_len:
            result.extend([0] * delta_len)

        for i in range(len(self)):
            result[i] += self[i]

        return result

    def __radd__(self, other: list):
        return self + other

    def __sub__(self, other: list):
        result = CustomList(self[:])
        delta_len = len(other) - len(result)
        if delta_len:
            result.extend([0] * delta_len)

        for i in range(len(other)):
            result[i] -= other[i]

        return result

    def __rsub__(self, other: list):
        return CustomList(other) - self

    def __str__(self):
        return f"items: {', '.join(map(str, self))}; sum: {sum(self)}"

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)


if __name__ == "__main__":
    print([5, 1, 3, 7] - CustomList([1, 2, 7]))
