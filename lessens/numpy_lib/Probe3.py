import numpy as np

a, b = 6, 9

print(bool(b > a))
print(bool(b >= a))
print(bool(a == b))

ages = np.array([
    [15, 23, 32, 45, 52],
    [68, 34, 55, 78, 20],
    [25, 67, 33, 45, 14]
])

print(ages)
print('старше 15:\n', ages >= 16)

work = (ages > 18) & (ages < 60)
print('старше 18 и младше 60:\n', work)
print('кол-во: ', work.sum())

work = (ages < 18) | (ages > 60)
print('младше 18 или старше 60:\n', work)
print('кол-во: ', work.sum())

print('старше 15:\n', ages[ages >= 16])
print('старше 15 и младше 60:\n', ages[(ages >= 16) & (ages < 60)])
