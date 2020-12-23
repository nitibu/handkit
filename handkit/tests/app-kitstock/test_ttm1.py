import datetime
import logging
from decimal import Decimal

import baostock as bs
import pytest
from django.test import TestCase, Client
from django.utils import timezone

from kitstock.models import StockKData


class TestBaoStock(object):
    logger = logging.getLogger(__name__)
    lg = bs.login()
    
    def __del__(self):
        bs.logout()
        
    def test_client(self):
        client = Client()
        response = client.get('/kitstock/stock_base')
        print(response.content)
    
    def test_now(self):
        print(timezone.now().strftime("%Y-%m-%d"))
    
    # 获取滚动市盈率
    def test_ttm(self):
        rs = bs.query_history_k_data("sh.600999", "code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM,date")
        # result = list()
        while (rs.error_code == '0') & rs.next():
            print(rs.get_row_data())



if __name__ == '__main__':
    pytest.main(['-q', 'test_ttm.py'])
