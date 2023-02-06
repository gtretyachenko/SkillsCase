# !/usr/bin/python3
# -*- coding: utf-8 -*-

# *********Импорт системных библиотек***************
import os
from abc import ABC
# import sys
# from pathlib import Path
# from datetime import datetime
# # Импорт почтового сервера
# import smtplib
# # Импорт библиотек конструктора электронных писем
# from email import message
# # Импорт библиотек конструктора электронных писем
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
# from email.mime.multipart import MIMEMultipart
# from email.header import Header
# import re
# import numpy as np
# import pandas as pd
import pymysql as sql
from pymysql import Error
import configparser as cnf


# ///////////////Config.ini//////////////////////////
class ConfigConnector(object):

    def __init__(self):
        self.path_to_me = os.path.abspath(os.curdir) + r'\config.ini'
        self._connect = cnf.ConfigParser()
        if os.path.exists(self.path_to_me):
            try:
                self._connect.read(self.path_to_me)
                self.read_settings()
            except BaseException as exp:
                print(f'Файл поврежден config.ini err:{exp}')
        else:
            try:
                raise ValueError
            except ValueError as exp:
                print(f'В проекте отсутствует файл config.ini err:{exp}')

    def read_settings(self):
        res = {}
        for page in self._connect.sections():
            res[page] = {}
            for head in self._connect.options(page):
                res[page][head] = self._connect.get(page, head)
        if res:
            pass
        return res

    def get_settings(self, page, header):
        return self._connect.get(page, header)

    # def add_settings(self, page, headers=None, values=None):
    #     if headers:
    #         if len(headers) == len(values):
    #             for head, val in headers, values:
    #                 self._connect.set(page, head, val)
    #         else:
    #             return None
    #     else:
    #         self._connect.add_section(page)
    #     with open(self.path_to_me, "w") as config_file:
    #         self._connect.write(config_file)
    #
    # def change_setting(self, page, headers, new_values):
    #     for head, val in headers, new_values:
    #         self._connect.set(page, head, val)
    #     with open(self.path_to_me, "w") as config_file:
    #         self._connect.write(config_file)
    #
    # def del_setting(self, page, headers=None):
    #     if headers:
    #         self._connect.remove_section(page)
    #     else:
    #         for head in headers:
    #             self._connect.remove_option(page, head)
    #     with open(self.path_to_me, "w") as config_file:
    #         self._connect.write(config_file)


# ////////////////////////////MY SQL//////////////////////////
class MySqlConnector(object):
    config = ConfigConnector()

    def __init__(self, env=None):
        self._connect = None
        self.df_headers = None
        if not env:
            try:
                self.db_host = MySqlConnector.config.get_settings('mysql', 'host')
                self.db_port = MySqlConnector.config.get_settings('mysql', 'port')
                self.db_user = MySqlConnector.config.get_settings('mysql', 'user')
                self.db_pwd = MySqlConnector.config.get_settings('mysql', 'password')
                self.db_name = MySqlConnector.config.get_settings('mysql', 'db_name')
            except BaseException as exc:
                print(f'Ошибка чтения файла конфига {MySqlConnector.config.path_to_me} err: {exc}')
            self._connect = sql.connect(host=self.db_host, port=int(self.db_port), user=self.db_user,
                                        password=self.db_pwd, charset='utf8', db=self.db_name,
                                        init_command='set names utf8')
            print('----------------------Подключение с сервером MYSQL открыто!----------------------\n')

    def get_table_headers(self, df_name):
        _sql = f'''
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHARE TABLE_NAME = {df_name}
        '''
        return self.execute_read_query(_sql)

    def execute_read_query(self, query):
        cursor = self._connect.cursor()
        result = None
        try:
            cursor.execute(query)
            self.df_headers = [i[0] for i in cursor.description]
            result = cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
        return result

    def execute_query(self, query):
        cursor = self._connect.cursor()
        try:
            cursor.execute(query)
            self._connect.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def execute_many_query(self, query, val):
        cursor = self._connect.cursor()
        try:
            cursor.executemany(query, val)
            self._connect.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

    def query_all(self, query, params=None):
        cursor = self._connect.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.df_headers = [i[0] for i in cursor.description]
            result = cursor.fetchall()
        finally:
            cursor.close()
        return result


# ////////////////////////////SEND TO EMAIL//////////////////////////
class EMailConnector:
    config = ConfigConnector()
    pass


# //////////////////////////TASKS MANAGER////////////////////////////
class DataTask(MySqlConnector, ABC):
    list_temp_files = []
    to_pdf = []

    @staticmethod
    def read_data_frame(source, df_name):
        if source == 'SQL':
            connection_to_mysql = MySqlConnector()
            _sql = '''
                SELECT * FROM {table_name}
                
            '''.format(table_name=df_name)
            return connection_to_mysql.execute_query(_sql)
        elif source == 'CSV':
            pass
            return
        elif source == 'XLSX':
            pass
            return
        elif source == 'TXT':
            pass
            return

    @staticmethod
    def transform_data_frame(df, method):
        pass

    @staticmethod
    def load_to_sql(df, tbl_name, method):
        connection_to_mysql = MySqlConnector()
        str_headers = connection_to_mysql.get_table_headers(tbl_name).join(',')
        str_val = '%s,' * str_headers.count(',')
        if method == "REP":
            _sql = f'''REPLACE {str_headers} INTO {tbl_name} VALUES {str_val} '''
            connection_to_mysql.execute_many_query(_sql, df)
        elif method == "INS":
            _sql = f'''INSERT INTO {tbl_name} VALUES {str_val} '''
            connection_to_mysql.execute_many_query(_sql, df)
        elif method == "SET":
            pass

    @staticmethod
    def call_sql_procedure(procedure_name):
        connection_to_mysql = MySqlConnector()
        procedure_name + connection_to_mysql  # STOP!
        pass

    @staticmethod
    def eda_analitics(filename=None, to_pdf=None):
        if not to_pdf:
            if not filename:
                DataTask().__create_df_temp_file(DataTask.list_temp_files[-1])
            else:
                DataTask().__excute_ipynb_to_pdf(filename)
        pass

    @staticmethod
    def __create_df_temp_file(filename):
        try:
            DataTask.list_temp_files.append(filename)
            pass
        except BaseException as exc:
            print(f'Не возможно сохранить временный файл: {filename} err: {exc}')

    @staticmethod
    def __excute_ipynb_to_pdf(filename=None):
        if not filename:
            filename = DataTask.list_temp_files[-1]
        try:
            os.system(f'jupyter nbconvert --to webpdf --allow-chromium-download {filename}.ipynb')
        except BaseException as exc:
            print(f'Ошибка зауска файла {filename}.ipynb err: {exc}')


if __name__ == '__main__':
    etl = DataTask()
    etl.load_to_sql(
        df=etl.transform_data_frame(
            df=etl.read_data_frame(source='SQL', df_name='fact'), method='qwe'), tbl_name='', method='INS')
