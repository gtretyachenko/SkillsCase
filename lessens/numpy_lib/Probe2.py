import numpy as np

lst = [5, 4, 3, 5, 4, 3, 4]

# методы работы с одномерными масивами
marks = np.array(lst)
obj_list = [marks]
for el in obj_list:
    print(type(el))
    print(el)
    print(el.min())
    print(el.max())
    print(el.mean())
    print(el.argmin())
    print(el.argmax())

# методы работы с джвумерными масивами
grades = np.array([
    [3, 5, 5, 4, 3],
    [3, 3, 4, 3, 3],
    [5, 5, 5, 4, 3]

])
obj_list = [grades]
for el in obj_list:
    print(type(el))
    print(el)
    print(el.min())
    print(el.max())
    print(el.mean(axis=1))
    print(el.mean(axis=0))
    print(el.argmin())
    print(el.argmax())

# генерация одномерных массивов
range_arr = np.arange(2, 9)
obj_list = [range_arr]
for el in obj_list:
    print(type(el))
    print(el)
    print(el.min())
    print(el.max())
    print(el.mean())
    print(el.mean())
    print(el.argmin())
    print(el.argmax())

# генерация 1массива для графика функции х = у2
range_arr = np.arange(1, 11, 0.5)
range_arr **= 2
obj_list = [range_arr]
for el in obj_list:
    print(type(el))
    print(el)
    print(el.min())
    print(el.max())
    print(el.mean())
    print(el.mean())
    print(el.argmin())
    print(el.argmax())

# генерация массивов 0 - нолей и 1 - едениц

zer_arr = np.zeros((3, 3))
one_arr = np.ones((4, 2))
eye_arr = np.eye(5)  # еденичная матрица row=col
zer_arr **= 2
obj_list = [zer_arr, one_arr, eye_arr]
for el in obj_list:
    print(type(el))
    print(el)
    print(el.min())
    print(el.max())
    print(el.mean())
    print(el.mean())
    print(el.argmin())
    print(el.argmax())
