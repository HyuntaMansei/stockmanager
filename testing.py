from pykiwoom.kiwoom import Kiwoom

kiwoom = Kiwoom()
kiwoom.CommConnect()

from kiwoom_manager import KiwoomManager
km = KiwoomManager(kiwoom)

km.market_clas_dic
km.rev_market_clas_dic
km.stock_info