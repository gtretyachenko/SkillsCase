from termcolor import cprint


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


def txt_to_list(txt_name, sep):
    f = None
    rows = []
    i = 0
    try:
        f = open(txt_name, 'r', encoding="utf-8")
        lines = f.readlines()
        for line in lines:
            res = line.strip()
            rows.append([*res.split(sep)])
            i += 1
    except FileNotFoundError as exc:
        cprint(f'Файл txt не не найден: {exc}', color='red')
        # raise
    else:
        cprint(f'\n-------------Чтнение файла: {txt_name}-------------\nНайдено {i} строк: ', color='green')
    finally:
        if f is not None:
            f.close()
    return rows


def list_to_txt(txt_name, source):
    my_file = None
    try:
        my_file = open(txt_name, 'w', encoding='utf-8')
        my_file.write('\n'.join(source))
    except BaseException as exc:
        cprint(exc, color='red')
    else:
        cprint(f'\nФайил {txt_name} создан', color='green')
        cprint(f'Кол-во строк в в файле: {len(source)}', color='green')
    finally:
        if my_file is not None:
            my_file.close()


# Старт процедуры проверки списка регистраций txt
good_logs, bad_logs = [], []
i = 0

registrations = txt_to_list(txt_name='registrations_ (1).txt', sep=' ')
for reg in registrations:
    i += 1
    print(', '.join(reg), f'строка {i}', sep=' => ')
    try:
        if len(reg) != 3:
            raise ValueError('НЕ присудствуют все 3 поля ValueError')
        if not reg[0].isalpha():
            raise NotNameError(
                'поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)')
        if '@' and '.' not in reg[1]:
            raise NotEmailError(
                'поле email НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)')
        if isinstance(reg[2], int) and reg[2] >= 10 and reg[2] <= 99:
            raise ValueError(
                'поле возраст НЕ является числом от 10 до 99: ValueError Вызов метода обернуть в try-except.')
    except BaseException as exc:
        cprint(f'{exc.args[0]} строка {i}', color='red')
        bad_logs.append(' '.join(reg))
    else:
        good_logs.append(' '.join(reg))

# создаем лог файлы
list_to_txt(txt_name='registrations_bad.log', source=bad_logs)
list_to_txt(txt_name='registrations_good.log', source=good_logs)
