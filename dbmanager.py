#mysql db와 연결하여 data를 처리하는 클래스
import configparser
import pymysql
import os

config = configparser.ConfigParser()
conf_path = os.getcwd() + os.sep + 'ignore' + os.sep + 'config.ini'
config.read(conf_path, encoding='utf-8')

con = config['DB_CONFIG']

class DbManager:
    def __init__(self):
        self.cnx = pymysql.connect(
            user=con['user'], password=con['password'], host=con['host'], port=int(con['port']),
            charset=con['charset'], db=con['db']
        )
        self.cur = self.cnx.cursor()

    def write_stock_info(self, stock_info: {}):
        for key, info in stock_info.items():
            sql = """
            insert into STOCK_BASIC_INFO_TB 
            (stock_code, stock_name, market_clas, created_date) 
            values (%s, %s, %s, NOW())
            on duplicate key update 
            stock_name = values(stock_name), market_clas = values(market_clas), is_updated = 'y', updated_date = now();
            """
            data = (key, info['name'], info['clas'])
            self.cur.execute(sql, data)
        self.cnx.commit()

    def exec_sql(self, sql, data=''):
        if not data == '':
            self.cur.execute(sql, data)
            self.cnx.commit()
        else:
            self.cur.execute(sql)
            self.cnx.commit()

    def show_table(self):
        sql = "show tables;"
        self.cur.execute(sql)