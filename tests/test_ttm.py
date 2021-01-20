import datetime
import json
import logging
from decimal import Decimal

import baostock as bs
import pandas as pd
import pytest
from django.test import TestCase
from django.utils import timezone

class TestBaoStock(object):
    logger = logging.getLogger(__name__)
    lg = bs.login()
    
    def __del__(self):
        bs.logout()
    
    @pytest.mark.django_db(transaction=True)
    def test_store_kdata(self):
        self.get_stock_kdata("sh.600999")
    
    def test_now(self):
        print(timezone.now().strftime("%Y-%m-%d"))
    
    # 获取滚动市盈率
    def test_ttm(self):
        rs = bs.query_history_k_data("sh.600999", "code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM,date")
        # result = list()
        while (rs.error_code == '0') & rs.next():
            print(rs.get_row_data())
    
    def test_getstocknumber(self):
        # 获取指定日期的指数、股票数据
        stock_rs = bs.query_all_stock(day="2020-12-01")
        stock_df = stock_rs.get_data()
        stock_df.to_csv('./all_list.csv', encoding='utf8', index=False)
        # stock_df.drop(stock_df[stock_df.code < 'sh.600000'].index, inplace=True)
        # stock_df.drop(stock_df[stock_df.code > 'sz.399000'].index, inplace=True)
        # xxx = stock_df.to_json()
        # self.logger.info(xxx)
        # stock_df = stock_df['code']
        # # stock_df.to_csv('./stk_data/stk_list.csv', encoding='utf8', index=False)
        # stockList = stock_df.tolist()
        # self.logger.info(json.dumps(stockList))
        
    def test_now(self):
        print(datetime.datetime.now().date())


if __name__ == '__main__':
    pytest.main(['-q', 'test_ttm.py'])
