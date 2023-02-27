import configparser
import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine

import numpy
import re
import IPython

# 디버깅 모드 설정. 쥬피터 노트에서 실행중인지 확인.
if 'IPKernelApp' in IPython.Application.instance().__class__.__name__:
    debug_mode = True
else:
    debug_mode = False

def debug(msg, flag_id:str ='0'):
    debugging_flags = '1'
    if flag_id in debugging_flags and debug_mode:
        print(msg)

#mysql db와 연결하여 data를 처리하는 클래스
config = configparser.ConfigParser()
# conf_path = os.getcwd() + os.sep + 'ignore' + os.sep + 'config.ini'
# conf_path = r'C:\Users\jchoi\Coding\python\stockmanager\ignore\config.ini'
conf_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'ignore' + os.sep + 'config.ini'
config.read(conf_path, encoding='utf-8')
con = config['DB_CONFIG']

class DbManager:
    def __init__(self):
        debug(con)
        self.connect()
    def connect(self):
        self.conn = pymysql.connect(
            user=con['user'], password=con['password'], host=con['host'], port=int(con['port']),
            charset=con['charset'], db=con['db']
        )
        self.cur = self.conn.cursor()
    def close(self):
        debug("Testing close")
        debug(conn)
        self.conn.close()
    def get_column_names_of_tb(self, table_name)-> list:
        column_names = []
        # Get the column names from a table named "table_name"
        self.cur.execute(f"SHOW COLUMNS FROM {table_name}")
        column_names = [x[0] for x in self.cur.fetchall()]
        # self.cur.description
        # for x in self.cur.fetchall():
        #     print(x)
        return  column_names
    def write_krx_daily_stock_price_dmi(self):
        info = {}
        info['from_table_name'] = 'temp_tb'
        info['to_table_name'] = 'daily_stock_price_tb'
        info['from_column_names'] = [
            '티커', '종목명', '시장이름', '소속부', '시가', '고가', '저가', '종가',
            '전일대비', '등락률', '거래량', '거래대금', '상장주식수'
        ]
        info['to_column_names'] = [
            'stock_code', 'stock_name', 'market', 'department', 'open_price', 'high_price', 'low_price', 'close_price',
            'cmpared_prev_price', 'fluctuation_rate', 'trading_volume', 'trading_value', 'listed_shared'
        ]
        self.write_data_matching_information_tb(info)
    def write_data_matching_information_tb(self, info: dict):
        ftn = info['from_table_name']
        ttn = info['to_table_name']
        fcn: list = info['from_column_names']
        tcn: list = info['to_column_names']
        for i in range(len(fcn)):
            dup_test = ' from '.join([fcn[i], ftn, ttn])
            print(dup_test)
            sql = f"""
            INSERT INTO data_matching_information_tb (
            dup_test, from_table_name, to_table_name, from_column_name, to_column_name, created_date
            ) values (
            %s, %s, %s, %s, %s, NOW()
            ) on duplicate key update 
            to_table_name=value(to_table_name), to_column_name=value(to_column_name), updated_date=now(), is_updated='y'
            """
            data = (dup_test, ftn, ttn, fcn[i], tcn[i])
            debug(sql)
            debug(data)
            debug("Before executing sql")
            self.exec_sql(sql, data)
        self.conn.commit()

    def move_data_using_dmi(self, info: dict):

        from_table_name = info['from_table_name']
        from_column_names = info['from_column_names']
        to_table_name = info['to_table_name']
        to_column_names = info['to_column_names']

        # 날짜삽입하는 구문
        from_column_names.append('now()')
        to_column_names.append('created_date')
        #on duplicate key update
        odku_clause = self.get_odku_clause(info['to_column_names'])

        fcn_str = ', '.join(from_column_names)
        tcn_str = ', '.join(to_column_names)
        # DB내에서 from에서 to로 데이터를 옮기는 쿼리
        sql = f"""
        insert into {to_table_name} (
            {tcn_str} 
        )
        select {fcn_str}
        from {from_table_name}
        on duplicate key update {odku_clause}
        """

        debug(sql, '1')
        self.exec_sql(sql)
    def connect_using_create_engine(self, conx_info: dict):
        p = str('mysql+pymysql://') + str(conx_info['user']) + ':' + conx_info['password'] + '@' + conx_info['host'] + ':' + conx_info['port'] + '/' + conx_info['db']
        debug(p)
        db_connection = create_engine(p)
        return db_connection
    def write_data_frame(self, df: pd.DataFrame):
        db_connection = self.connect_using_create_engine(con)
        df.to_sql(name='temp_tb', con=db_connection, if_exists='replace', index=True)
    def write_and_move_data_frame(self, ttn: str, df: pd.DataFrame):
        db_connection = self.connect_using_create_engine(con)
        table_name = 'temp_tb'
        df.to_sql(name=table_name, con=db_connection, if_exists='replace', index=True)

        fcns = self.get_column_names_of_tb(table_name)
        info = {
            'from_table_name': table_name,
            'from_column_names': fcns,
            'to_table_name': ttn
        }
        info['to_column_names'] = self.get_to_column_names(info)

        self.move_data_using_dmi(info)
    def get_to_column_names(self, info: dict) -> dict:
        tcnl = []
        for fcn in info['from_column_names']:
            sql = """
            select to_column_name from data_matching_information_tb
            where from_table_name = %s and from_column_name = %s and to_table_name = %s; 
            """
            data = (info['from_table_name'], fcn, info['to_table_name'])

            debug(sql)
            debug(data)

            self.exec_sql(sql, data)
            tcnl.append(self.fetch_one()[0])
        return tcnl

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
            );
            """
            data = (code)
            self.cur.execute(sql, data)
        self.conn.commit()
    def get_odku_clause(self, inserting_column_names: list):
        #칼럼 이름에서 created_time은 없어야 함.
        temp = []
        for cn in inserting_column_names:
            temp.append(f'{cn} = values({cn})')
        temp.append("is_updated='y', updated_date=now()")
        odku_clause = ', '.join(temp)
        debug(odku_clause)
        return odku_clause

    def exec_sql(self, sql, data=''):
        if not data == '':
            self.cur.execute(sql, data)
            self.conn.commit()
        else:
            self.cur.execute(sql)
            self.conn.commit()
    def fetch_one(self):
        result = self.cur.fetchone()
        return result
    def fetch_all(self):
        result = self.cur.fetchall()
        return result
    def show_table(self):
        sql = "show tables;"
        self.cur.execute(sql)
    def __del__(self):
        self.close()
        debug("Exiting dbManager")

    def make_sample_info(self)-> dict:
        info = {}
        info['from_table_name'] = 'temp_tb'
        info['to_table_name'] = 'daily_stock_price_tb'
        info['from_column_names'] = [
            '티커', '종목명', '시장이름', '소속부', '시가', '고가', '저가', '종가',
            '전일대비', '등락률', '거래량', '거래대금', '상장주식수'
        ]
        info['to_column_names'] = [
            'stock_code', 'stock_name', 'market', 'department', 'open_price', 'high_price', 'low_price', 'close_price',
            'cmpared_prev_price', 'fluctuation_rate', 'trading_volume', 'trading_value', 'listed_shares'
        ]
        return info