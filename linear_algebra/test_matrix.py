from matrix import Matrix


print('0 iteration')

a = Matrix([[1, 2, 3], [4, 5, 6]])
assert [d for d in a] == [1, 2, 3, 4, 5, 6]
print(a.T())
print(a.T)

print('1 creation')
a = Matrix([[1, 2], [3, 4]])
b = Matrix.filled(rows=2, cols=3, value=0)


print('2 printing')
a = Matrix([[1, 2], [3, 4]])
assert str(a) == '[[1, 2],\n[3, 4]]'


print('3 data readout')
a = Matrix([[1, 2], [3, 4]])
assert a.data == [[1, 2], [3, 4]]
try:
    a.data = [[0, 0], [0, 0]]
    raise AssertionError('Exception was not raised!')
except AttributeError:
    pass

internal = a.data
internal[0][0] = 42
assert a.data == [[1, 2], [3, 4]]

print('4 access and modify')
a = Matrix([[1, 2], [3, 4]])
assert a[0, 0] == 1
assert a[1, 0] == 3

a[0, 1] = 42
assert a.data == [[1, 42], [3, 4]]

print('5 transpose')
a = Matrix([[1, 2], [3, 4]])
b = a.T

assert isinstance(b, Matrix)
assert b.data == [[1, 3], [2, 4]]

a[0, 0] = 42
assert b.data == [[1, 3], [2, 4]]

print('6 addition')
a = Matrix([[1, 2], [3, 4]])
b = Matrix.filled(2, 2, 1)
c = a + b

assert isinstance(c, Matrix)
assert c.data == [[2, 3], [4, 5]], c

print('7 scalar multiplication')
a = Matrix([[1, 2], [3, 4]])
b = 2 * a

assert isinstance(b, Matrix)
assert b.data == [[2, 4], [6, 8]]

print('8 matrix multiplication')
a = Matrix([[1, 2]])
b = Matrix([[3], [4]])

c = a * b
d = b * a

assert isinstance(c, Matrix)
assert isinstance(d, Matrix)
assert c.data == [[11]]
assert d.data == [[3, 6], [4, 8]]
