from pykrx import stock
from time import sleep

class pykrxManager:
    def __init__(self):
        self.market_list = [
            'KOSPI',
            'KOSDAQ',
            'KONEX'
        ]
        self.market_ticker_list_dic = {}
        self.basic_stock_info_dic = {}

    def set_market_ticker_list_dic(self):
        for m in self.market_list:
            self.market_ticker_list_dic[m] = stock.get_market_ticker_list(market=m)

    def get_basic_stock_info(self)-> {}:
        for m in self.market_list:
            for t in self.market_ticker_list_dic[m]:
                self.basic_stock_info_dic[t] = {
                    'name': stock.get_market_ticker_name(t),
                    'market': m
                }
                sleep(0.05)
        return self.basic_stock_info_dic