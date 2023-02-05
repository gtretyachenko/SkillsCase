# -*- coding: utf-8 -*-
from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime
import qlikfunctions

tasksDict = {
    u'NP. CSV Выгрузка дневных отчетов ГД': {
        'Pool': 'np_default_pool',  # default_pool (10 слотов), heavy_etl_pool(1 слот), sensors (100 слотов)
        'Soft': 'np1',  # qv1/qv2/np/qs
        'TaskId': 'e1aa8b2c-c453-49dd-95f7-76f6955ab972',  # id задачи внутри NP, именно - app_id !
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        # 'StartTime' : [5,27] , # время запуска, если не задано - то будет запущено после зависимостей, нельзя ставить лидирующие нули
        # 'Dep' : [ # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
        #      u'QV1. Мониторинг обновления',
        #      u'QV1. Консоль QMC',
        # ] ,
        'Retries_count': 3,  # количество запусков при фэйле таска
        'Retries_delay': 120,  # интервал перезапуска в секундах
    },
    u'QV1. EMR_DailyGD_Reports': {
        'Pool': 'qv1_default_pool',
        'Soft': 'qv1',
        'TaskId': '532ec72e-6fe9-438b-a0c1-0528aa6bebec',
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'NP. CSV Выгрузка дневных отчетов ГД',
        ],
        'Retries_count': 3,  # количество запусков при фэйле таска
        'Retries_delay': 120,  # интервал перезапуска в секундах
    },
    u'NP. Рассылка дневных отчетов ГД part1': {
        'Pool': 'np_default_pool',  # default_pool (10 слотов), heavy_etl_pool(1 слот), sensors (100 слотов)
        'Soft': 'np1',  # qv1/qv2/np/qs
        'TaskId': ['875896f3-4343-441a-a591-a73f9ac1277a',
                   '88dce7cc-3be2-48ae-9fe9-1029b618c73b',
                   '5e0057a1-ea67-4264-aecc-05734ab98c23',
                   '35b6bb91-8823-484d-9a4f-164b7a7128af',
                   '9a52fa4b-bebb-4792-8761-2154ffbe576f',
                   'f75f65f3-ffb4-4166-8f1d-21711dcf70d6',
                   '672075e0-dcda-4f75-9569-3258e1fe893a',
                   '2c932718-e7f3-46f0-ad49-6e3e105f902b',
                   'a06bdba3-b6ab-4081-9123-ac4d90e4adf5',
                   '749e987f-45e0-4c38-be87-3b0c57495113'],
        # id задачи внутри NP, именно - app_id !, # id задачи внутри NP, именно - app_id !
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'RandomStartDelay': 120,  # в секундах, произвольное ожидание перед запуском основного скрипта в таске
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'QV1. EMR_DailyGD_Reports',
        ],
        'Retries_count': 3,  # количество запусков при фэйле таска
        'Retries_delay': 120,  # интервал перезапуска в секундах
    },
    u'virtual sleep1': {  # Имя - любое
        'Soft': 'sleep',  # ключевой параметр
        'TaskId': u'1',
        # 'Pool' : 'sensors', уже не используем
        'Seconds': 120,  # ключевой параметр - целое число
        'Dep': [
            u'QV1. EMR_DailyGD_Reports',
        ],
    },

    u'NP. Рассылка дневных отчетов ГД part2': {
        'Pool': 'np_default_pool',  # default_pool (10 слотов), heavy_etl_pool(1 слот), sensors (100 слотов)
        'Soft': 'np1',  # qv1/qv2/np/qs
        'TaskId': ['34f38a23-e014-4780-807c-0191933d100f',
                   'c43f41b2-7a61-42de-8c1c-e109776dda48',
                   'a32501da-8649-46ff-b7a1-8e619c009a27',
                   'dd9496e5-fd81-48f5-a18f-a9f5a32a12c8',
                   '2646891d-38fc-4e10-9b5b-695c8e84f361',
                   '51c05642-d175-437b-a05d-6fc703b8f55f',
                   '7350dfa8-7cd2-4f3c-bdd3-d62cc1b51ec4',
                   '73fbc585-263f-4746-b355-17b9d5e601c3',
                   'e1c69829-f53c-48bf-9740-f8e0ab4e4da6',
                   'df071fa8-0a08-4a74-8775-79b11e77c299',
                   # 'a5205d45-8f5e-47db-96d7-1b91ab48f271',
                   '62d3e5cc-6f58-458e-b7db-904cd3a0396c'],
        # id задачи внутри NP, именно - app_id !, # id задачи внутри NP, именно - app_id !
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'RandomStartDelay': 120,  # в секундах, произвольное ожидание перед запуском основного скрипта в таске
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'virtual sleep1',
        ],
        'Retries_count': 3,  # количество запусков при фэйле таска
        'Retries_delay': 120,  # интервал перезапуска в секундах
    },

    u'QV1. Контроль содержимого отчетов ГД': {
        'Pool': 'qv1_default_pool',
        'Soft': 'qv1',
        'TaskId': '90c2156f-f434-4919-aa43-bcabb52c1b23',
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'NP._Рассылка_дневных_отчетов_ГД_part1_f75f65f3-ffb4-4166-8f1d-21711dcf70d6',
        ],
    },
    u'NP. Проверки дневных отчетов ГД': {
        'Pool': 'np_default_pool',  # default_pool (10 слотов), heavy_etl_pool(1 слот), sensors (100 слотов)
        'Soft': 'np1',  # qv1/qv2/np/qs
        'TaskId': '7d707f7b-c961-4b3c-ae26-8bfb546878b2',  # id задачи внутри NP, именно - app_id !
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'QV1. Контроль содержимого отчетов ГД',
        ],
    },
    u'QV1. Проверка сортировки в отчетах ГД': {
        'Pool': 'qv1_default_pool',
        'Soft': 'qv1',
        'TaskId': 'bd92280d-f586-48b4-8963-9cc4d65532c2',
        'OnFail': {'mail': 'qlik@luding.ru'},  # mail address to send msg
        'Dep': [  # завимости от других тасков, предшествующих, пока они не выполнятся - запуск этого таска не начнётся
            u'NP._Рассылка_дневных_отчетов_ГД_part1_f75f65f3-ffb4-4166-8f1d-21711dcf70d6',
        ],
    },
}

# Аргументы по-умолчанию
default_args = {
    'owner': 'ushakov',
    'depends_on_past': False,
    # 'retries': 0,
    # 'retries': 1,
}
# раписание шедулера можно смотреть тут: https://crontab.guru/
# время UTC !!!
# Описание DAG'а - https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/index.html#airflow.models.DAG
# Параметры DAG'а
dag = DAG(
    dag_id='_GD_Reports_Daily',  # под этим именем в AF будет отображаться задание
    default_args=default_args,
    start_date=datetime(2020, 1, 1, 0, 0, 0, 0),  # Дата начала
    # schedule_interval = '@daily', # Как часто запускать
    schedule_interval=None,
    description='Daily GD Reports',  # Описание DAG'а
    tags=['nprinting', 'qlikview'],  # Тэги DAG'а
    catchup=False
)

airflowTasksDict = {}
qlikfunctions.create_tasks(tasksDict, airflowTasksDict, dag)
