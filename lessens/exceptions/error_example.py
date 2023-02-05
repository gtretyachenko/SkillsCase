def div():
    for i in range(2):
        try:
            x = int(input("enter a number: "))
            y = int(input("enter another number: "))
            print(x, '/', y, '=', x / y)
        except (ValueError, ZeroDivisionError) as exc:
            if isinstance(exc, ValueError):
                print(f'Ошибка, получено НЕ целое число {exc}')
            if isinstance(exc, ZeroDivisionError):
                print(f'Ошибка вычисления, деление на ноль: {exc}')


# div()

# ValueError: invalid literal for int() with base 10: 'f'
# ZeroDivisionError: division by zero

def sumOfPairs(L1, L2):
    try:
        sum = 0
        sumOfPairs = []
        for i in range(len(L1)):
            sumOfPairs.append(L1[i] + L2[i])
        print("sumOfPairs = ", sumOfPairs)
    except (TypeError, IndexError) as exc:
        if isinstance(exc, TypeError):
            print(f'Ошибка, объект нетого типа: {exc}')
        if isinstance(exc, IndexError):
            print(f'Ошибка, индекс обекта не найден (размер L2 != L1): {exc}')


n1, n2 = 1, 1
sumOfPairs(L1=n1, L2=n2)

# TypeError: object of type 'int' has no len()
# IndexError: list index out of range
