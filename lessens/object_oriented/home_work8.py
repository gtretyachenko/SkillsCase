# Напишите класс Fraction для работы с дробями. Пусть дробь в нашем классе предстает в виде числитель/знаменатель.
# Дробное число должно создаваться по запросу Fraction(a, b), где a – это числитель, а b – знаменатель дроби.
# Добавьте возможность сложения (сложения через оператор сложения) для дроби. Предполагается,
#     что операция сложения может проводиться как только между дробями, так и между дробью и целым числом.
# Результат операции должен быть представлен в виде дроби.
# Добавьте возможность взятия разности (вычитания через оператор вычитания) для дробей.
# Предполагается, что операция вычитания может проводиться как только для двух дробей,
#     так и для дроби и целого числа. Результат операции должен быть представлен в виде дроби.
# Добавьте возможность умножения (умножения через оператор умножения) для дробей. Предполагается,
#     что операция умножения может проводиться как только для двух дробей, так и для дроби и целого числа.
# Результат операции должен быть представлен в виде дроби.
# Добавьте возможность приведения дроби к целому числу через стандартную функцию int().
# Добавьте возможность приведения дроби к числу с плавающей точкой через стандартную функцию float().
# Создайте дочерний класс OperationsOnFraction и добавьте туда собственные методы getint и getfloat,
#     которые будут возвращать целую часть дроби и представление дроби в виде числа с плавающей точкой соответственно.

# -*- coding: utf-8 -*-

# Калькулятор дробей дробей (модель)
class OperationsOnFraction:

    def getint(self):
        int_egr = int(self.c)
        return int_egr

    def getfloat(self):
        flt = float(self.c + self.a / self.b)
        return flt


class Fraction(OperationsOnFraction):

    def __init__(self, a=0, b=0, c=0, mod=''):
        # '''Объект дробь'''
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        self.mod = mod

    def __add__(self, other):
        # '''Сложение дробей '''
        # преобразование дробей
        s = Fraction.__transform(self)
        o = Fraction.__transform(other)
        # если общий знаменатель
        mod = ''
        if s.b == o.b:
            a = s.a + o.a
            b = s.b
            c = s.c + o.c
            # если дробь не правильная
            if a > b:
                c += a // b
                a = a % b
                # если числитель 0
                if a == 0:
                    b = 0
                return Fraction(a=a, b=b, c=c).simplify()
            # если дробь правильная
            return Fraction(a=a, b=b, c=c).simplify()
        # наименьший общий знаменатель
        lcd = Fraction.__get_lcd(s.b, o.b)
        ab1 = lcd / s.b
        ab2 = lcd / o.b
        a = s.a * ab1 + o.a * ab2
        c = s.c + o.c
        # если дробь не правильная
        if a > lcd:
            c += a // lcd
            a = a % lcd
            return Fraction(a=a, b=lcd, c=c).simplify()
        # если дробь правильная
        return Fraction(a=a, b=lcd, c=c).simplify()

    def __sub__(self, other):
        # '''Вычитание дробей '''
        # преобразование дробей
        s = Fraction.__transform(self)
        o = Fraction.__transform(other)
        # если общий знаменатель
        mod = ''
        if s.b == o.b:
            a = (s.c * s.b + s.a) - (o.c * o.b + o.a)
            b = s.b
            c = 0
            # модуль доби
            if a < 0:
                mod = '-'
                a = -a
            # если дробь не правильная
            if a > b:
                c = a // b
                a = a % b
                # если числитель 0
                if a == 0:
                    b = 0
                return Fraction(a=a, b=b, c=c, mod=mod).simplify()
            # если дробь правильная
            return Fraction(a=a, b=b, c=c, mod=mod).simplify()
        # наименьший общий знаменатель
        lcd = Fraction.__get_lcd(s.b, o.b)
        ab1 = lcd / s.b
        ab2 = lcd / o.b
        a = (s.a * ab1) - (ab2 * o.a)
        c = s.c - o.c
        # модуль доби
        if a < 0:
            mod = '-'
            a = -a
        # модуль доби
        if c < 0:
            mod = '-'
            c = -c
        # если дробь не правильная
        if a > lcd:
            c = a // lcd
            a = a % lcd
            # если числитель 0
            if a == 0:
                lcd = 0
            return Fraction(a=a, b=lcd, c=c, mod=mod).simplify()
        # если дробь правильная
        return Fraction(a=a, b=lcd, c=c, mod=mod).simplify()

    def __mul__(self, other):
        # '''Умножение дробей '''
        # преобразование дробей
        s = Fraction.__transform(self)
        o = Fraction.__transform(other)
        # вычисление
        mod = ''
        a = (s.c * s.b + s.a) * (o.c * o.b + o.a)
        b = s.b * o.b
        c = 0
        # модуль доби
        if a < 0:
            mod = '-'
            a = -a
        # если дробь не правильная
        if a > b:
            c = a // b
            a = a % b
            # если числитель 0
            if a == 0:
                b = 0
            return Fraction(a=a, b=b, c=c, mod=mod).simplify()
        # если дробь правильная
        return Fraction(a=a, b=b, c=c, mod=mod).simplify()

    def __int__(self):
        int_egr = int(self.c)
        return int_egr

    def __float__(self):
        flt = float(self.c + self.a / self.b)
        return flt

    @staticmethod
    def __get_nod(args):
        # получение НОД от чисел
        r, res, i = 1, 1, 2
        ab = args[:i]
        while i <= len(args):
            if i == 2:
                a, b = ab
            else:
                a, b = res, args[i - 1]
            while r > 0:
                if a > b:
                    r = a % b
                    a, b = b, r
                    res = a
                else:
                    r = b % a
                    b, a = a, r
                    res = b
            i += 1
            r = 1
        return res

    @staticmethod
    def __get_lcd(b1, b2):
        # приведение 2х чисел к общему знаменателю
        cd1, cd2 = b1, b2
        if b1 > b2:
            cd1, cd2 = b2, b1
        x = cd2
        while x % cd1 > 0 or x % cd2 > 0:
            x += 1
        return x

    @staticmethod
    def __transform(abc):
        # преобразование целого числа в дробь
        if isinstance(abc, int):
            abc = Fraction(a=0, b=0, c=abc)
        a = int(abc.a)
        b = int(abc.b)
        c = int(abc.c)
        # пробразование дроби от целого
        if a == 0 and b == 0:
            a = int(c)
            b = 1
            c = 0
        return Fraction(a=a, b=b, c=c)

    def simplify(self):
        # '''Упрощение дроби через НОД'''
        a = self.a
        b = self.b
        if a < 0:
            a = -a
        if a + b == 0:
            return self
        nod = Fraction.__get_nod([a, b])
        self.a = a // nod
        self.b = b // nod
        # если дробь не правильная
        if a > b:
            c = a // b
            a = a % b
            # если числитель 0
            if a == 0:
                b = 0
            self.a = a
            self.b = b
            self.c = c
            return self
        return self


# Калькулятор дробей дробей (реализация)
action_list = ['+', '-', '*', 's', 'int', 'flt']


def get_fraction():
    i = 0
    a, b, c = 0, 0, 0
    while i == 0:
        c = int(input('Введите целое дроби: '))
        a = int(input('Введите числитель дроби: '))
        b = int(input('Введите знаменатиль дроби: '))
        if isinstance(c + a + b, int):
            i = 1
    fraction = Fraction(a=a, b=b, c=c)
    print(f'Обявили дробь {fraction.c} целых {fraction.a} {fraction.b}-ых')
    return fraction


def choice_action(act_list):
    i = 0
    act = ''
    while i == 0:
        act = input('Выбирети двействие (+ сложить, - вычесть, * умножить, s упросить, int целое, flt флоат): ')
        if act in act_list:
            i = 1
    return act


fraction1 = get_fraction()
action = choice_action(action_list)
if action in action_list[:3]:
    print(f'Укажите вторую дробь для действия {action} :')
    fraction2 = get_fraction()
    if action == '+':
        # Сложение дробей
        sum_fraction = fraction1 + fraction2
        print(f'Сложили {fraction1.c} целых {fraction1.a} {fraction1.b}-ых и {fraction2.c} целых'
              f' {fraction2.a} {fraction2.b}-ых \nполучили {sum_fraction.c} целых '
              f'{sum_fraction.a} {sum_fraction.b}-ых'
              )
    elif action == '-':
        # Вычитание дробей
        sub_fraction = fraction1 - fraction2
        print(f'Вычли из {fraction1.c} целых {fraction1.a} {fraction1.b}-ых дробь {fraction2.c} целых'
              f' {fraction2.a} {fraction2.b}-ых \nполучили {sub_fraction.mod} {sub_fraction.c} целых '
              f'{sub_fraction.a} {sub_fraction.b}-ых'
              )
    if action == '*':
        # Умножение дробей
        mul_fraction = fraction1 * fraction2
        print(f'Умножили {fraction1.c} целых {fraction1.a} {fraction1.b}-ых на дробь {fraction2.c} целых'
              f' {fraction2.a} {fraction2.b}-ых \nполучили {mul_fraction.mod} {mul_fraction.c} целых '
              f'{mul_fraction.a} {mul_fraction.b}-ых'
              )
if action == 's':
    # Упрощение дробей
    s_fraction = fraction1.simplify()
    print(f'Получили {s_fraction.mod} {s_fraction.c} целых '
          f'{s_fraction.a} {s_fraction.b}-ых')

if action == 'int':
    # Целое число от дроби
    print(f'Получили {fraction1.getint()} целых')
    # тестирование переопределенных спец методов
    print('спец методом init():', int(fraction1))

if action == 'flt':
    # флоат дроби
    print(f'Получили {fraction1.getfloat()}')
    # тестирование переопределенных спец методов
    print('спец методом float():', float(fraction1))
