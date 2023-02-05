import os

path = r'C:\Users\GTretyachenko\Desktop\Лист Microsoft Excel.xlsx'
start = path.startswith('C:')
end = path.endswith('xlsx')

# print(path, start, end)

user = 'GTretyachenko'
path = os.path.join(os.path.abspath('/'), 'Users', user, 'Desktop')
print(path)

past_count = 0
temp_count = 0
dirs = []
while True:
    i = 1
    for elem in os.listdir(path):
        i += 1
        if elem.endswith('.tmp'):
            temp_count += 1
        dirs.append([elem, os.path.islink(elem)])

    if past_count != 0 and i != past_count:
        print('Рабочий стол изменен!')
        break
    past_count = i
    print('***********************', '\nКоличество директорий рабочего стола:{}'.format(past_count))
    print('Кол-во временных файлов:{}'.format(temp_count))
    print('Список всех объектов:')
    for dir in dirs:
        print(dir[0])
    break
