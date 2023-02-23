from pykiwoom.kiwoom import Kiwoom

#pykiwoom lib를 이용하여 키움증권에서 증권 정보를 얻어 옴.
class KiwoomManager:
    #초기화하면서 각 종목의 정보에 대해서 받아 옴
    def __init__(self, kiwoom: Kiwoom) -> None:
        #키움접속은 클래스 외부에서 하기로
        self.kiwoom = kiwoom

        #stock_info는 code로 name과 clas를 매칭.
        self.stock_info = {}
        self.market_clas_dic = {}
        self.rev_market_clas_dic = {}

        self.set_basic_stock_info()
        self.set_market_clas()

    def set_basic_stock_info(self):
        self.all_code_list = self.kiwoom.GetCodeListByMarket('')
        self.all_name_list = []
        self.all_market_clas = []
        #value[0] = 종목명, value[1] = 시장구

        for code in self.all_code_list:
            name = self.kiwoom.GetMasterCodeName(code)
            self.all_name_list.append(name)

        #code로 stock종목 보는 딕셔너리 구성. 우선 clas는 빈칸으로 설정.
        for i in range(len(self.all_code_list)):
            self.stock_info[self.all_code_list[i]] = {
                'name': self.all_name_list[i],
                'clas':''
            }

    def set_market_clas(self):
        # 시장 구분에 대한 딕셔너리. 각 키에 대해서 키 값과 밸류 튜플.(리스트가 나을려나?)
        self.market_clas_dic = {
            #   [시장구분값]
            '0': 'KOSPI',
            '10': 'KOSDAQ',
            '3': 'ELW',
            '8': 'ETF',
            '50': 'KONEX',
            '4': '뮤추얼펀드',
            '5': '신주인수권',
            '6': '리츠',
            '9': '하이얼펀드',
            '30': 'K-OTC'
        }
        #거꾸로된 딕셔너리도 구비
        self.rev_market_clas_dic = self.invert_dic(self.market_clas_dic)

        # 모든 시장 구분 값에 따른 코드 리스트를 딕셔너리로 구성
        self.code_list_dic_by_market_clas = {}  # key는 시장구분값, value는 코드리스트
        for key in self.market_clas_dic.keys():
            self.code_list_dic_by_market_clas[key] = self.kiwoom.GetCodeListByMarket(key)

        # stock_info 딕셔너리의 clas 부분 수정
        for code in self.all_code_list:
            self.stock_info[code]['clas'] = self.get_market_clas(code)

    def get_market_clas(self, code):
        clas = ''
        # ETN 예외 처리
        if 'ETN' in self.stock_info[code]['name']:
            return 'ETN'

        for key, code_list in self.code_list_dic_by_market_clas.items():
            if code in code_list:
                # print(f'Found match, clas: {key}')
                clas = key
                #break하지 않음. 코스피에 있는 다른 종류의 증권 때문에.

        clas_name = self.market_clas_dic[clas]
        return clas_name

    def invert_dic(self, dic):
        inv_dic = {}
        for key, value in dic.items():
            inv_dic[value] = key

        return inv_dic

    def testing(self):
        print("Testing")


