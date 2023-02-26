import configparser
import os
import pymysql
import pandas
import numpy
import re

#mysql db와 연결하여 data를 처리하는 클래스
config = configparser.ConfigParser()
# conf_path = os.getcwd() + os.sep + 'ignore' + os.sep + 'config.ini'
conf_path = r'C:\Users\jchoi\Coding\python\stockmanager\ignore\config.ini'
config.read(conf_path, encoding='utf-8')
con = config['DB_CONFIG']

class DbManager:
    def __init__(self):
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(
            user=con['user'], password=con['password'], host=con['host'], port=int(con['port']),
            charset=con['charset'], db=con['db']
        )
        self.cur = self.conn.cursor()
    def close(self):
        self.conn.close()
    def write_basic_stock_info(self, stock_info: {}):
        for k, v in stock_info.items():
            sql = """
            insert into basic_stock_info_tb 
            (stock_code, stock_name, market, created_date) 
            values (%s, %s, %s, NOW())
            on duplicate key update 
            stock_name = values(stock_name), market = values(market), is_updated = 'y', updated_date = now();
            """
            data = (k, v['name'], v['market'])
            self.cur.execute(sql, data)
        self.conn.commit()

    def write_daily_stock_price(self, dsp):
        for code in dsp.index:
            sql = """
            insert into daily_stock_price_tb (
            stock_code
            )
            values (
            %s 
            )
            """
            data = (code)
            self.cur.execute(sql, data)
        self.conn.commit()
    def exec_sql(self, sql, data=''):
        if not data == '':
            self.cur.execute(sql, data)
            self.conn.commit()
        else:
            self.cur.execute(sql)
            self.conn.commit()
    def show_table(self):
        sql = "show tables;"
        self.cur.execute(sql)