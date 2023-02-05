# -*- coding: utf-8 -*-
try:
    import os
    from time import sleep
    import json
    import requests
    import random
    from datetime import timedelta
    from requests_ntlm import HttpNtlmAuth
    from zeep import Client
    from zeep.transports import Transport
    from airflow import DAG
    from airflow.exceptions import AirflowException
    from airflow.utils.log.logging_mixin import LoggingMixin
    from airflow.utils.dates import days_ago
    from airflow.sensors.time_delta import \
        TimeDeltaSensor  # qv_np_default.py:17 DeprecationWarning: This module is deprecated. Please use `airflow.sensors.time_delta`.
    from airflow.operators.python import PythonOperator
    from airflow.providers.telegram.hooks.telegram import TelegramHook
    import ast
    import csv
except Exception as e:
    print("Error {}".format(e))


# читаем настройки из файла
def read_config():
    file = '/home/airflow/airflow/dags/config.json'
    with open(file, 'r') as f:
        config = json.load(f)
    return config


config = read_config()  # читаем конфиг с настройками


def onsuccess_func(*args, **kwargs):
    pass
    # telegram_hook = TelegramHook(token=telegramToken, chat_id=telegramChat)
    # telegram_hook.send_message({"text": "Hello from airflow hook"})


def onfail_func(*args, **kwargs):
    # telegramToken = config["telegram"]["token"]
    pass


def sendlog_telegram(msg):
    telegram_hook = TelegramHook(token=config["telegram"]["token"], chat_id=config["telegram"]["chats"]["chernov"])
    telegram_hook.send_message({"text": msg})
    pass


def sleep_task(*args, **kwargs):
    sleep_seconds = kwargs.get('sleep_timer')
    sleep(sleep_seconds)


'''
Broken DAG: [/home/airflow/airflow/dags/_qs_task_extractor.py] Traceback (most recent call last):
  File "/home/airflow/airflow/dags/qlikfunctions.py", line 609, in create_tasks
    AirflowTask = create_aftask(task, task_id, tasksDict[task]["TaskId"], dag, tasksDict)
  File "/home/airflow/airflow/dags/qlikfunctions.py", line 476, in create_aftask
    "certificate" : config[tasksDict[task]['Soft']]["certificate"],
KeyError: 'get_qs_tasks'
'''


def get_qs_tasks(*args, **kwargs):
    qs_server = kwargs.get('qs_server')
    qs_username = kwargs.get('qs_username')
    qs_password = kwargs.get('qs_password')
    qs_filename = kwargs.get('qs_filename')

    xrfkey = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnm1234567890', 16))

    # print (xrfkey)
    qs_headers = {
        'content-type': 'application/json',
        'X-Qlik-Xrfkey': xrfkey,
        'X-Qlik-User': 'UserDirectory=INTERNAL; UserId=sa_repository',
    }

    certificate = ('/home/airflow/airflow/certs/client.pem',
                   '/home/airflow/airflow/certs/client_key.pem')
    root = '/home/airflow/airflow/certs/root.pem'

    requests.packages.urllib3.disable_warnings()

    qs_session = requests.session()
    qs_session.auth = HttpNtlmAuth(qs_username, qs_password, qs_session)

    # запуск релоада
    endpoint = 'qrs/task/full'

    def byte_to_dict(txt):
        dict_str = txt.decode("UTF-8").replace('\\\\', '\\').replace(':null', ':""').replace(':false',
                                                                                             ':False').replace(':true',
                                                                                                               ':True')
        mydata = ast.literal_eval(dict_str)
        return mydata

    url = '{0}:4242/{1}?Xrfkey={2}'.format(qs_server, endpoint, xrfkey)
    start_response = qs_session.get(url, headers=qs_headers, verify=False, cert=certificate)

    if start_response.status_code == 200:
        content = byte_to_dict(start_response.content)
        # print (qs_filename, content,sep='\n\n\n\n\n')
        print('Tasks total count = {}'.format(len(content)))

        result_list = []

        for task in content:
            # print (task)
            content = {}
            content["task_id"] = task["id"]
            content["task_name"] = task["name"]
            content["task_enabled"] = task["enabled"]
            content["task_timeout"] = task["taskSessionTimeout"]
            content["task_retries"] = task["maxRetries"]
            content["app_id"] = task["app"].get("id")
            content["app_name"] = task["app"].get("name")
            if type(task["app"].get("stream")) is dict:
                content["stream_id"] = task["app"]["stream"].get("id")
                content["stream_name"] = task["app"]["stream"].get("name")
            elif type(task["app"].get("stream")) is str:
                content["stream_id"] = ''
                content["stream_name"] = ''

            result_list.append(content)
            # print ('\n' * 5)

        print('Total items in list = {}'.format(len(result_list)))
        # print (result_list)

        # for i in content:
        #    print (i,sep='\n')
        # print (type(content[0]))
        # print (content[0])

        # with open(qs_filename, 'w') as f:
        #    json.dump(content,f)
    else:
        raise AirflowException('Response give !=200 status_code\n', start_response.content)

    with open(qs_filename, 'w', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, restval="-", fieldnames=result_list[0].keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(result_list)


def qs_run_task(*args, **kwargs):
    qs_server = kwargs.get('qs_server')
    qs_username = kwargs.get('qs_username')
    qs_password = kwargs.get('qs_password')
    qs_taskid = kwargs.get('qs_taskid')

    random_delay = kwargs.get('random_delay')
    if random_delay != None:
        random.seed()
        secs = random.random() * random_delay
        print('Random delay in seconds - {}'.format(secs))
        sleep(secs)

    # sendlog_telegram('Таск запущен')
    # raise AirflowException ('test')

    xrfkey = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnm1234567890', 16))

    # print (xrfkey)
    qs_headers = {
        'content-type': 'application/json',
        'X-Qlik-Xrfkey': xrfkey,
        'X-Qlik-User': 'UserDirectory=INTERNAL; UserId=sa_repository',
    }

    certificate = ('/home/airflow/airflow/certs/client.pem',
                   '/home/airflow/airflow/certs/client_key.pem')
    root = '/home/airflow/airflow/certs/root.pem'

    requests.packages.urllib3.disable_warnings()

    qs_session = requests.session()
    qs_session.auth = HttpNtlmAuth(qs_username, qs_password, qs_session)

    # запуск релоада
    endpoint = 'qrs/task/{}/start/synchronous'.format(qs_taskid)
    url = '{0}:4242/{1}?Xrfkey={2}'.format(qs_server, endpoint, xrfkey)
    start_response = qs_session.post(url, headers=qs_headers, verify=False, cert=certificate)

    def byte_to_dict(txt):
        dict_str = txt.decode("UTF-8").replace('\\\\', '\\').replace(':null', ':""').replace(':false',
                                                                                             ':False').replace(':true',
                                                                                                               ':True')
        mydata = ast.literal_eval(dict_str)
        return mydata

    if start_response.status_code != 201:
        raise AirflowException('Не удалось запустить задачу {}'.format(qs_taskid))

    session_id = byte_to_dict(start_response.content)["value"]
    if session_id == '00000000-0000-0000-0000-000000000000':
        raise AirflowException('Задача запущена или не удалось запустить таск {} внутри сессии'.format(qs_taskid))

    # получаем сессию в которой будет запуск таска
    endpoint = 'qrs/executionsession/{}'.format(session_id)
    url = '{0}:4242/{1}?Xrfkey={2}'.format(qs_server, endpoint, xrfkey)
    session_response = qs_session.get(url, headers=qs_headers, verify=False, cert=certificate)
    exec_id = byte_to_dict(session_response.content)["executionResult"]["id"]

    while True:

        endpoint = 'qrs/executionresult/{}'.format(exec_id)
        url = '{0}:4242/{1}?Xrfkey={2}'.format(qs_server, endpoint, xrfkey)
        exec_response = qs_session.get(url, headers=qs_headers, verify=False, cert=certificate)
        result = byte_to_dict(exec_response.content)

        allstatuses = ['0: NeverStarted', '1: Triggered', '2: Started', '3: Queued',
                       '4: AbortInitiated', '5: Aborting', '6: Aborted', '7: FinishedSuccess',
                       '8: FinishedFail', '9: Skipped', '10: Retry', '11: Error', '12: Reset']

        bad_status = [4, 5, 6, 8, 11, 12]
        good_status = [7]

        status = result["status"]
        if status in bad_status:
            raise AirflowException('Error status = {}\n'.format(status))
            break
        elif status in good_status:
            print('All complete!')
            break
        else:
            # print ('Current status = {}'.format(status))
            pass

        sleep(1)

    if kwargs.get('telegram_ok') != None:
        print('create hook')
        t = TelegramHook(token=config["telegram"]["token"], chat_id=kwargs.get('telegram_ok'))
        msg = 'Airflow alert: DAG: {}\nTASK: {}\nStatus : Completed\n'.format(kwargs.get('mydagid'),
                                                                              kwargs.get('mytaskid'))
        print(msg)
        t.send_message({"text": msg})

    # if kwargs.get('mail_ok') != None:
    #     msg = 'Airflow alert: DAG: {} | TASK: {} | Status : Completed'.format(kwargs.get('mydagid'),kwargs.get('mytaskid'))
    #     m = EmailOperator(to = kwargs.get('mail_ok'),subject=msg,html_content='Status : Completed',task_id = kwargs.get('mytaskid'))
    #     m.execute()

    # print ('Test kwargs - {}'.format(kwargs.get('telegram_ok')))


def qv_run_task(*args, **kwargs):
    config = read_config()
    qv_server = kwargs.get('qv_server')
    qv_port = kwargs.get('qv_port')
    qv_extraurl = kwargs.get('qv_extraurl')
    qv_username = kwargs.get('qv_username')
    qv_password = kwargs.get('qv_password')
    qv_taskid = kwargs.get('qv_taskid')
    qv_dsid = kwargs.get('qv_dsid')
    # qv_getstatustimeout = kwargs.get('qv_getstatustimeout')
    qv_getstatustimeout = None

    random_delay = kwargs.get('random_delay')
    if random_delay != None:
        random.seed()
        secs = random.random() * random_delay
        print('Random delay in seconds - {}'.format(secs))
        sleep(secs)

    session = requests.session()
    session.auth = HttpNtlmAuth(qv_username, qv_password)
    wsdl = "{0}:{1}{2}".format(qv_server, qv_port, qv_extraurl)
    client = Client(wsdl, transport=Transport(session=session))
    service_key = client.service.GetTimeLimitedServiceKey()
    client.transport.session.headers.update({'X-Service-Key': service_key})

    try:
        execute_status = client.service.TriggerEDXTask(qv_dsid, qv_taskid, '')
    except Exception as e:
        message = 'DAG: {}\nTASK: {}\nFailed to start QV task: {}\nERROR : {}'.format(kwargs.get('mydagid'),
                                                                                      kwargs.get('mytaskid'), qv_taskid,
                                                                                      e)
        raise AirflowException(message)

    check_sleep_time = 10  # seconds, sleep interval

    if qv_getstatustimeout != None:
        trycount_max = int(qv_getstatustimeout / check_sleep_time)

    trycount_errors = 0
    trycounter_total = 0
    while True:
        sleep(check_sleep_time)
        status = 'Unknown'
        try:
            service_key = client.service.GetTimeLimitedServiceKey()
            client.transport.session.headers.update({'X-Service-Key': service_key})
            task_status = client.service.GetEDXTaskStatus(qv_dsid, execute_status.ExecId)
            status = task_status.TaskStatus
            if task_status.TaskName[-15:] == '(work disabled)':
                raise AirflowException("QlikView task failed with status - QlikView task is disabled")
            if status == 'Completed':
                break
            if status == 'Warning':
                raise AirflowException("QlikView task failed with status - The task completed with a warning")
                break
            if status == 'Failed':
                raise AirflowException("QlikView task failed with status - Failed")
            if status == 'Aborting':
                raise AirflowException("QlikView task failed with status - Aborting")
            if status == 'Disabled':
                raise AirflowException(
                    "QlikView task failed with status - The task is about to run but hasn't started yet")
            if status == 'Unrunnable':
                raise AirflowException(
                    "QlikView task failed with status - The task has a distributiongroup unavailable")
        except Exception as e:
            message = 'DAG: {} | TASK: {} | Error when trying ({} (current)/{} (total)) to get the task status in QV: {}\nError text: {}'.format(
                kwargs.get('mydagid'), kwargs.get('mytaskid'), trycount_errors, trycounter_total, qv_taskid, e)
            if qv_getstatustimeout != None:
                if trycount_errors >= trycount_max:
                    raise AirflowException(message)
            else:
                raise AirflowException(message)
            trycount_errors += 1
        trycounter_total += 1

    # add remove files
    filelist = kwargs.get('delete_files')
    if filelist != None:
        for i in range(len(filelist)):
            if os.path.isfile(filelist[i]):
                print('Delete file : {}'.format(filelist[i]))
                os.remove(filelist[i])

    if kwargs.get('telegram_ok') != None:
        t = TelegramHook(token=config["telegram"]["token"], chat_id=kwargs.get('telegram_ok'))
        msg = 'Airflow alert: DAG: {}\nTASK: {}\nStatus : Completed\n'.format(kwargs.get('mydagid'),
                                                                              kwargs.get('mytaskid'))
        print(msg)
        t.send_message({"text": msg})


def np_run_task(*args, **kwargs):
    np_server = kwargs.get('np_server')
    np_credential = kwargs.get('np_credential')
    np_password = kwargs.get('np_password')
    np_taskid = kwargs.get('np_taskid')
    np_warnisfail = kwargs.get('np_warnisfail')
    if np_warnisfail == None:
        np_warnisfail = False

    random_delay = kwargs.get('random_delay')
    if random_delay != None:
        random.seed()
        secs = random.random() * random_delay
        print('Random delay in seconds - {}'.format(secs))
        sleep(secs)

    requests.packages.urllib3.disable_warnings()
    tokenstring = ''
    np_headers = {"Accept": "application/json",
                  "Content-Type": "application/json"}
    np_session = requests.session()

    np_session.auth = HttpNtlmAuth(np_credential, np_password, np_session)
    np_headers['User-Agent'] = 'Windows'
    # получаем авторизацию
    response = np_session.get('{0}/{1}'.format(np_server, 'login/ntlm'), headers=np_headers, verify=False)
    tokenstring = (np_session.cookies['NPWEBCONSOLE_XSRF-TOKEN'])
    np_headers['X-XSRF-TOKEN'] = tokenstring

    # print (response.json())
    # формируем запрос на запуск таска
    urltorun = '{0}/{1}/{2}/executions'.format(np_server, 'tasks', np_taskid)

    # добавил 60 попыток запустить таск NP
    attemps = 10
    for i in range(attemps):
        try:
            response = np_session.post(urltorun, headers=np_headers, verify=False)
            # print (response.json())
            result = response.json()["data"]
            break
        except Exception as e:
            if i == attemps - 1:
                print('Error {} attempt:\n{}\n{}\n{}'.format(attemps, e, response.json(), urltorun))
                raise AirflowException('Не удалось запустить NP task за {} попыток'.format(attemps))
            if i == 0:
                print('Error 0 attempt:\n{}\n{}\n{}'.format(e, response.json(), urltorun))

            # if i == 2:
            #     raise AirflowException('Не удалось запустить NP task за 3 попытки\nПоследняя ошибка: {}'.format(e))
            random.seed()
            secs = random.random() * 9 + 1
            print('Не удалось запустить NP task, попытка = {} с паузой {} сек.'.format(str(i + 1), secs))
            sleep(secs)

    # print (response["id"])
    # print (type(response))
    # print (response["id"])
    # из ответа получаем id запущенного таска
    np_exec_id = result["id"]
    # мониторим выполнение
    check_sleep_time = 10  # seconds
    while True:
        sleep(check_sleep_time)
        # result = np.check_task_status(np_taskid, np_exec_id)
        urltorun = '{0}/{1}/{2}/executions/{3}'.format(np_server, 'tasks', np_taskid, np_exec_id)
        response = np_session.get(urltorun, headers=np_headers, verify=False)
        result = response.json()["data"]
        if result["status"] == 'Completed':
            # sendlog_telegram ('{} - {} - Completed\n{}'.format ( {{ dag }}, {{ task }}, {{ ti }}))
            # sendlog_telegram ('Completed')
            break
        if result["status"] == 'Warning' and np_warnisfail == True:
            raise AirflowException("NPrinting task failed with status Warning, flag WarnIsFail = True")

        if result["status"] == 'Warning':
            # sendlog_telegram ('Warning')
            break
        if result["status"] == 'CompletedWithWarning':
            # sendlog_telegram ('Warning')
            break
        if result["status"] == 'Failed':
            raise AirflowException("NPrinting task failed with status Failed")
        if result["status"] == 'Aborted':
            raise AirflowException("NPrinting task failed with status Aborted")

        # WaitingForRetry
        # Enqueued
        # Assigned
        # Running
        # Completed
        # Aborting
        # Aborted
        # Failed
        # Timeout
        # Warning
        # Failing
        # CompletedWithWarning
    if kwargs.get('telegram_ok') != None:
        print('create hook')
        t = TelegramHook(token=config["telegram"]["token"], chat_id=kwargs.get('telegram_ok'))
        msg = 'Airflow alert: DAG: {}\nTASK: {}\nStatus : Completed\n'.format(kwargs.get('mydagid'),
                                                                              kwargs.get('mytaskid'))
        print(msg)
        t.send_message({"text": msg})


def clean_for_taskid(name):
    newname = name.replace(" ", "_").replace("'", "").replace("/", "_").replace("(", "_").replace(")", "_").replace(",",
                                                                                                                    "_").replace(
        ".qvw", "").replace("__", "_")
    return newname


def create_aftask(task, task_id, task_guid, dag, tasksDict):
    config = read_config()
    args_telegram_ok = None
    args_telegram_fail = None
    args_mail_ok = None
    args_mail_fail = None
    var_name = None  # for qv
    var_values = None  # for qv
    mydag = dag.dag_id
    mytaskid = task_id
    warningisfail = None
    random_delay = None
    delete_files = None
    args_getstatustimeout = None

    if tasksDict[task].get('OnSuccess') != None:
        if tasksDict[task].get('OnSuccess').get('telegram') != None:
            args_telegram_ok = tasksDict[task].get('OnSuccess').get('telegram')
        if tasksDict[task].get('OnSuccess').get('mail') != None:
            args_mail_ok = tasksDict[task].get('OnSuccess').get('mail')
    if tasksDict[task].get('OnFail') != None:
        if tasksDict[task].get('OnFail').get('telegram') != None:
            args_telegram_fail = tasksDict[task].get('OnFail').get('telegram')
        if tasksDict[task].get('OnFail').get('mail') != None:
            args_mail_fail = tasksDict[task].get('OnFail').get('mail')
    if tasksDict[task].get('WarningIsFail') != None:
        warningisfail = tasksDict[task].get('WarningIsFail')
    if tasksDict[task].get('RandomStartDelay') != None:
        random_delay = tasksDict[task].get('RandomStartDelay')
    if tasksDict[task].get('GetStatusTimeout') != None:
        args_getstatustimeout = tasksDict[task].get('GetStatusTimeout')
    if tasksDict[task].get('DeleteFiles') != None:
        delete_files = tasksDict[task].get('DeleteFiles')
        if type(delete_files) is not list:
            raise AirflowException(
                'In task {}, parameter "DeleteFiles" must be list, not {}'.format(task_id, str(type(delete_files))))

    # QS Get Task list
    if tasksDict[task]['Soft'] == 'get_qs_tasks':
        kwargs = {
            "qs_server": config[tasksDict[task]['Server']]["server"],
            "qs_username": config[tasksDict[task]['Server']]["username"],
            "qs_password": config[tasksDict[task]['Server']]["password"],
            "qs_filename": tasksDict[task].get('FullFileName_ToSave'),
            "certificate": config[tasksDict[task]['Soft']]["certificate"],
            # "root_cert" : config[tasksDict[task]['Soft']]["root_cert"],
            "mail_ok": args_mail_ok,
            "mail_fail": args_mail_fail,
            "telegram_ok": args_telegram_ok,
            "telegram_fail": args_telegram_fail,
            "mydagid": mydag,
            "mytaskid": mytaskid,
            "random_delay": random_delay,
        }
        AirflowTask = PythonOperator(task_id=task_id, python_callable=get_qs_tasks, op_kwargs=kwargs, dag=dag)

    # NPrinting
    if tasksDict[task]['Soft'][:2] == 'np':
        kwargs = {
            "np_server": config[tasksDict[task]['Soft']]["server"],
            "np_credential": config[tasksDict[task]['Soft']]["credential"],
            "np_password": config[tasksDict[task]['Soft']]["password"],
            "np_taskid": task_guid,
            "mail_ok": args_mail_ok,
            "mail_fail": args_mail_fail,
            "telegram_ok": args_telegram_ok,
            "telegram_fail": args_telegram_fail,
            "mydagid": mydag,
            "mytaskid": mytaskid,
            "np_warnisfail": warningisfail,
            "random_delay": random_delay,
            "delete_files": delete_files,
        }
        AirflowTask = PythonOperator(task_id=task_id, python_callable=np_run_task, op_kwargs=kwargs, dag=dag)

    # QlikView
    if tasksDict[task]['Soft'][:2] == 'qv':
        kwargs = {
            "qv_server": config[tasksDict[task]['Soft']]["server"],
            "qv_port": config[tasksDict[task]['Soft']]["port"],
            "qv_extraurl": config[tasksDict[task]['Soft']]["extraurl"],
            "qv_username": config[tasksDict[task]['Soft']]["username"],
            "qv_password": config[tasksDict[task]['Soft']]["password"],
            "qv_taskid": task_guid,
            "qv_getstatustimeout": args_getstatustimeout,
            "mail_ok": args_mail_ok,
            "mail_fail": args_mail_fail,
            "telegram_ok": args_telegram_ok,
            "telegram_fail": args_telegram_fail,
            "mydagid": mydag,
            "mytaskid": mytaskid,
            "random_delay": random_delay,
            "delete_files": delete_files,
        }
        AirflowTask = PythonOperator(task_id=task_id, python_callable=qv_run_task, op_kwargs=kwargs, dag=dag)

        # Qlik Sense
    if tasksDict[task]['Soft'][:2] == 'qs':
        kwargs = {
            "qs_server": config[tasksDict[task]['Soft']]["server"],
            "qs_username": config[tasksDict[task]['Soft']]["username"],
            "qs_password": config[tasksDict[task]['Soft']]["password"],
            "certificate": config[tasksDict[task]['Soft']]["certificate"],
            # "root_cert" : config[tasksDict[task]['Soft']]["root_cert"],
            "qs_taskid": task_guid,
            "mail_ok": args_mail_ok,
            "mail_fail": args_mail_fail,
            "telegram_ok": args_telegram_ok,
            "telegram_fail": args_telegram_fail,
            "mydagid": mydag,
            "mytaskid": mytaskid,
            "random_delay": random_delay,
            "delete_files": delete_files,
        }
        AirflowTask = PythonOperator(task_id=task_id, python_callable=qs_run_task, op_kwargs=kwargs, dag=dag)
        # Sleep timer
    if tasksDict[task]['Soft'] == 'sleep':
        kwargs = {
            "sleep_timer": tasksDict[task]["Seconds"],
        }
        sensorSeconds = tasksDict[task]["Seconds"]
        sensorTaskID = task_guid + '_sleep_{}'.format(str(sensorSeconds))
        AirflowTask = PythonOperator(task_id=sensorTaskID, python_callable=sleep_task, op_kwargs=kwargs, dag=dag,
                                     pool='sensors')

    return AirflowTask


def addparams_totask(task, newtask, dag, tasksDict, airflowTasksDict):
    if 'Dep' in tasksDict[task]:
        for dep in tasksDict[task]['Dep']:
            airflowTasksDict[newtask].set_upstream(airflowTasksDict[dep])  # перед чем должно быть выполнено

    if 'OnFail' in tasksDict[task]:
        if tasksDict[task]['OnFail'].get('mail') != None:
            airflowTasksDict[newtask].email_on_failure = True
            airflowTasksDict[newtask].email = tasksDict[task]['OnFail']['mail']
            # sendlog_telegram('Send error in task({}) to email : {} '.format(task,tasksDict[task]['OnFail']["mail"]))

    if 'Retries_count' in tasksDict[task]:
        airflowTasksDict[newtask].retries = int(tasksDict[task]['Retries_count'])
    if 'Retries_delay' in tasksDict[task]:
        airflowTasksDict[newtask].retry_delay = timedelta(seconds=int(tasksDict[task]['Retries_delay']))

    if 'Retries_ExponentialDelay' in tasksDict[task]:
        airflowTasksDict[newtask].retry_exponential_backoff = tasksDict[task]['Retries_ExponentialDelay']

    # if 'Priority' in tasksDict[task]:
    #     airflowTasksDict[task].priority_weight = tasksDict[task]['Priority']

    if 'StartTime' in tasksDict[task]:
        hour = tasksDict[task]['StartTime'][0]
        minute = tasksDict[task]['StartTime'][1]
        sensorTime = timedelta(hours=hour, minutes=minute)
        sensorTaskID = u'TimeSensor_{}_{}'.format(hour, minute)

        if sensorTaskID not in airflowTasksDict:
            SensorTask = TimeDeltaSensor(delta=sensorTime, task_id=sensorTaskID, pool='sensors', dag=dag)
            airflowTasksDict[sensorTaskID] = SensorTask
        airflowTasksDict[newtask].set_upstream(airflowTasksDict[sensorTaskID])

    if 'Pool' in tasksDict[task]:
        setpool = tasksDict[task]['Pool']
        airflowTasksDict[newtask].pool = setpool
    else:  # default pool from config if not manually set
        setpool = config[tasksDict[task]['Soft']]['default_pool']
        airflowTasksDict[newtask].pool = setpool


def create_tasks(tasksDict, airflowTasksDict, dag):
    for task in tasksDict.keys():

        if 'Soft' in tasksDict[task]:
            if type(tasksDict[task]["TaskId"]) is str:
                task_id = clean_for_taskid(task)
                AirflowTask = create_aftask(task, task_id, tasksDict[task]["TaskId"], dag, tasksDict)
                airflowTasksDict[task] = AirflowTask
                addparams_totask(task, task, dag, tasksDict, airflowTasksDict)
            elif type(tasksDict[task]["TaskId"]) is list:
                for i in range(len(tasksDict[task]["TaskId"])):
                    task_id = clean_for_taskid(task + '_' + str(tasksDict[task]["TaskId"][i]))
                    AirflowTask = create_aftask(task, task_id, str(tasksDict[task]["TaskId"][i]), dag, tasksDict)
                    airflowTasksDict[task_id] = AirflowTask
                    addparams_totask(task, task_id, dag, tasksDict, airflowTasksDict)
