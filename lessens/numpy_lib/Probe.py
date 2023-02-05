import numpy as np

use_list = [0.63, 0.75, 0.45]
first_array = np.array(use_list)

print(type(use_list))
print(use_list)
use_list = list(map(lambda x: x * 100, use_list))
print(use_list)
use_list = list(x * 100 for x in use_list)
print(use_list)

print(type(first_array))
print(first_array)
first_array *= 100
print(first_array)

week1 = np.array([4000, 0, 2000, 0, 1200])
week2 = np.array([1000, 2000, 0, 0, 3500])
print(week1 ** 2)

m21 = np.array([
    [2],
    [6],
    [1]
])

m22 = np.array([
    [2, 5],
    [6, 8],
    [1, 3]
])

m23 = np.array([
    [2, 5, 7],
    [6, 8, 5],
    [1, 3, 1]
])

m31 = np.array([
    [[2], [7]],
    [[6], [5]],
    [[1], [1]]
])

m32 = np.array([
    [[2, 5], [7, 5]],
    [[6, 8], [5, 8]],
    [[1, 3], [1, 3]]
])

m33 = np.array([
    [[2, 5, 7], [7, 5, 2]],
    [[6, 8, 5], [5, 8, 6]],
    [[1, 3, 1], [1, 3, 1]]
])

l_arrs = [m21, m22, m23, m31, m32, m33]

for i in l_arrs:
    print(type(i))
    print(i)
    print(i.ndim)
    print(i.shape)
    print(i.size)
    print(i[::2])
