import random


def list_deepcopy(l):
    # листр компрехэншен - генерация нового листа от старого через цикл с условием если в значениях есть еще листы то рекурссия
    return [elem if not isinstance(elem, list) else list_deepcopy(elem) for elem in l]


def change_dict(dct):
    num = random.randint(1, 100)
    for i_key, i_value in dct.items():
        if isinstance(i_value, list):
            # j_value = i_value[::] - вариант копирования листа через слайс
            j_value = i_value.copy()  # через метод copy
            j_value.append(num)
            dct[i_key] = j_value

        elif isinstance(i_value, dict):
            j_value = i_value.copy()  # через метод copy
            j_value[num] = i_key
            dct[i_key] = j_value
        elif isinstance(i_value, set):
            j_value = i_value.copy()  # через метод copy
            j_value.add(num)
            dct[i_key] = j_value


list_1 = [9, 8, 7]
deep_list = [1, 2, 3, list_1]
nums_list = [1, 2, 3]
some_dict = {1: 'text', 2: 'another text'}
uniq_nums = {1, 2, 3}
common_dict = {1: nums_list, 2: some_dict, 3: uniq_nums, 4: (10, 20, 30)}

change_dict(common_dict)
deep_list_copy = list_deepcopy(deep_list)
print(deep_list_copy is deep_list)
print(common_dict)
print(nums_list)
print(some_dict)
print(uniq_nums)


# -----------------------------------------------------------------------------------------

def read_obj(i_obj):
    if isinstance(i_obj, list):
        print(f' Тип данных: {i_obj.__class__.__name__} (лист)\n', 'Изменяемый (mutable)\n', f'Id объекта: {id(i_obj)}',
              end='\n')

    elif isinstance(i_obj, dict):
        print(f' Тип данных: {i_obj.__class__.__name__} (словарь)\n', 'Изменяемый (mutable)\n',
              f'Id объекта: {id(i_obj)}', end='\n')

    elif isinstance(i_obj, set):
        print(f' Тип данных: {i_obj.__class__.__name__} (множество)\n', 'Изменяемый (mutable)\n',
              f'Id объекта: {id(i_obj)}', end='\n')

    elif isinstance(i_obj, str):
        print(f' Тип данных: {i_obj.__class__.__name__} (строка)\n', 'Неизменяемый (immutable)\n',
              f'Id объекта: {id(i_obj)}', end='\n')

    elif isinstance(i_obj, int):
        print(f' Тип данных: {i_obj.__class__.__name__} (число)\n', 'Неизменяемый (immutable)\n',
              f'Id объекта: {id(i_obj)}', end='\n')

    elif isinstance(i_obj, tuple):
        print(f' Тип данных: {i_obj.__class__.__name__} (тьюпл)\n', 'Неизменяемый (immutable)\n',
              f'Id объекта: {id(i_obj)}', end='\n')


read_obj(list_1)
read_obj(some_dict)
read_obj(uniq_nums)
read_obj(1)
read_obj('qwerty')
read_obj((10, 20, 30))
