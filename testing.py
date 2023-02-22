# from pykiwoom.kiwoom import * 


# temp_kospi_code_list = kiwoom.GetCodeListByMarket('3') 
# kosdaq_code_list = kiwoom.GetCodeListByMarket('10')
# etf_code_list = kiwoom.GetCodeListByMarket('8')
# reit_code_list = kiwoom.GetCodeListByMarket('6')

temp_kospi_code_list = ['abc', 'aa_ETN'] #ETN 제거 필요
kospi_code_list = []
etn_code_list = []

# ETN 종목 제거
for c in temp_kospi_code_list:
    if 'ETN' in c:
        etn_code_list.append(c) #ETN리스트는 사용하지 않음
    else:
        kospi_code_list.append(c)