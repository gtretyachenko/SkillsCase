import math
import datetime

# последовательность Фибоначи 1, 1, 2, 3, 5, 8, 13, 21, ...

# Решение в лоб по формуле


n = int(input('Введите номер числа Фиббоначи: '))
now = datetime.datetime.now().microsecond
n = (((1 + math.sqrt(5)) / 2) ** n - ((1 - math.sqrt(5)) / 2) ** n) / math.sqrt(5)
now = datetime.datetime.now().microsecond - now
print('Расчет в лоб:', int(n), now)

# Решение циклом


n = int(input('Введите номер числа Фиббоначи: '))
now = datetime.datetime.now().microsecond
f1, f2, count = 0, 1, 0
while count < n:
    f1, f2 = f2, f1 + f2
    count += 1
now = datetime.datetime.now().microsecond - now
print('Расчет в циклом:', f1, now)


# Решение рекурсией


def get_num_fibbonacci(num=0):
    if num == 1 or num == 2:
        return 1
    else:
        return get_num_fibbonacci(num - 1) + get_num_fibbonacci(num - 2)


n = int(input('Введите номер числа Фиббоначи: '))
now = datetime.datetime.now().microsecond
res = get_num_fibbonacci(num=n)
now = datetime.datetime.now().microsecond - now
print('Расчет рекурсией:', res, now)
