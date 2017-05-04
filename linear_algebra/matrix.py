class Matrix:

    def __init__(self, data):
        if isinstance(data, type(self)):
            self._data = data.data
        else:
            self._data = data

    @staticmethod
    def filled(rows, cols, value=0):
        return Matrix([[value] * cols for r in range(rows)])

    def __str__(self):
        return '[' + ',\n'.join(str(r) for r in self.data) + ']'

    @property
    def data(self):
        return [r.copy() for r in self._data]

    def __len__(self):
        try:
            return len(self._data) * len(self._data[0])
        except IndexError:
            return 0

    def __iter__(self):
        for i in range(len(self)):
            yield(self[i])

    def __getitem__(self, key):
        try:
            return self._data[key[0]][key[1]]
        except TypeError:
            stride = len(self._data[0])
            return self._data[key // stride][key % stride]

    def getitem(self, key):
        if isinstance(key, tuple):
            return self._data[key[0]][key[1]]
        stride = len(self._data[0])
        return self._data[key // stride][key % stride]

    def __setitem__(self, key, value):
        try:
            self._data[key[0]][key[1]] = value
        except TypeError:
            stride = len(self._data[0])
            self._data[key // stride][key % stride] = value

    @property
    def T(self):
        return Matrix([list(c) for c in zip(*self.data)])

    def __add__(self, other):
        result = Matrix(self)
        for i, val in enumerate(other):
            result[i] += val
        return result

    def __rmul__(self, other):
        if isinstance(other, type(self)):
            return other @ self
        return self * other

    def __mul__(self, other):
        if isinstance(other, type(self)):
            return self @ other
        result = Matrix(self)
        for i in range(len(result)):
            result[i] *= other
        return result

    def __matmul__(self, other):
        right = other.T
        result = Matrix.filled(len(self._data), len(right._data), 0)
        for i, row in enumerate(self._data):
            for j, col in enumerate(right._data):
                result[i, j] = sum(map(lambda x, y: y * x, row, col))
        return result

    def __rmatmul__(self, other):
        return self @ other
