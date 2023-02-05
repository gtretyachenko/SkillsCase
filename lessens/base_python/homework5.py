import csv
from dateutil import parser


# import datetime


def get_conversion(data_csv, cross_selection=None):
    result_dict = {}
    for row in data_csv:
        if cross_selection is None or cross_selection in row.values():
            if 'month_' + str(parser.parse(row['date']).month) not in result_dict:
                result_dict['month_' + str(parser.parse(row['date']).month)] = {row['page']: [1.0, 0.0, 0.0, 0.0]}
            else:
                if row['page'] not in result_dict['month_' + str(parser.parse(row['date']).month)]:
                    result_dict['month_' + str(parser.parse(row['date']).month)][row['page']] = [1.0, 0.0, 0.0, 0.0]
                else:
                    result_dict['month_' + str(parser.parse(row['date']).month)][row['page']][0] += 1
    for value_res in result_dict.values():
        value_res[start_page][1] = round(value_res[start_page][0] / value_res[start_page][0] * 100, 2)
        value_res[start_page][2] = 0.0
        value_res[start_page][3] = 0.0
        value_res[control_page_1][1] = round(value_res[control_page_1][0] / value_res[start_page][0] * 100, 2)
        value_res[control_page_1][2] = round(value_res[control_page_1][0] / value_res[control_page_1][0] * 100, 2)
        value_res[control_page_1][3] = 0.0
        value_res[control_page_2][1] = round(value_res[control_page_2][0] / value_res[start_page][0] * 100, 2)
        value_res[control_page_2][2] = round(value_res[control_page_2][0] / value_res[control_page_1][0] * 100, 2)
        value_res[control_page_2][3] = round(value_res[control_page_2][0] / value_res[control_page_2][0] * 100, 2)
        value_res[target_page][1] = round(value_res[target_page][0] / value_res[start_page][0] * 100, 2)
        value_res[target_page][2] = round(value_res[target_page][0] / value_res[control_page_1][0] * 100, 2)
        value_res[target_page][3] = round(value_res[target_page][0] / value_res[control_page_2][0] * 100, 2)
    return result_dict


# name.csv ниже нужно заменить на название csv файла, который вы хотите открыть
# now = datetime.datetime.now()
file_path = r'D:\Курс Data Scientist (SkillBox)\Data Scientist. Аналитика. Начальный уровень\7. Знакомство с' \
            r' задачей, понятие «конверсии»\click_stream3.csv'

start_page = '1_home_page'
control_page_1 = '2_search_page'
control_page_2 = '3_payment_page'
target_page = '4_payment_confirmation_page'

with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date', 'core', 'gender'])  # читаем файл
    total = get_conversion(data_csv=csv_reader, cross_selection=None)

with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date', 'core', 'gender'])  # читаем файл
    desktop = get_conversion(data_csv=csv_reader, cross_selection='Desktop')

with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date', 'core', 'gender'])  # читаем файл
    mobile = get_conversion(data_csv=csv_reader, cross_selection='Mobile')

with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date', 'core', 'gender'])  # читаем файл
    female = get_conversion(data_csv=csv_reader, cross_selection='Female')

with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date', 'core', 'gender'])  # читаем файл
    male = get_conversion(data_csv=csv_reader, cross_selection='Male')

print('************************Total conversion*******************************')
for i in range(len(total)):
    str_month = "month_" + str((i + 1))
    print('________________________{}_______________________________'.format(str_month))
    for element, value in total[str_month].items():
        print(element, value, sep=': ')

print('************************Desktop conversion*******************************')
for i in range(len(desktop)):
    str_month = "month_" + str((i + 1))
    print('________________________{}_______________________________'.format(str_month))
    for element, value in desktop[str_month].items():
        print(element, value, sep=': ')

print('************************Mobile conversion*******************************')
for i in range(len(mobile)):
    str_month = "month_" + str((i + 1))
    print('________________________{}_______________________________'.format(str_month))
    for element, value in mobile[str_month].items():
        print(element, value, sep=': ')

print('************************Female conversion*******************************')
for i in range(len(female)):
    str_month = "month_" + str((i + 1))
    print('________________________{0}_______________________________'.format(str_month))
    for element, value in female[str_month].items():
        print(element, value, sep=': ')

print('************************Male conversion*******************************')
for i in range(len(male)):
    str_month = "month_" + str((i + 1))
    print('________________________{}_______________________________'.format(str_month))
    for element, value in male[str_month].items():
        print(element, value, sep=': ')

# now = datetime.datetime.now() - now
# print(now)
