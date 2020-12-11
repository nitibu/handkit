import datetime
import logging
from decimal import Decimal

import baostock
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

from kitstock.models import StockKData, StockInfoBase


class StockKDataView(View):
    logger = logging.getLogger(__name__)
    lg = baostock.login()
    
    def __del__(self):
        baostock.logout()
        
    def _compare_stock_date(self, kdata, exists):
        '''
            循环遍历已经存在的数据，如果kdata和任意一个数据的date一致，返回True
        '''
        for item in exists:
            aware_date = timezone.make_aware(datetime.datetime.strptime(kdata[6], '%Y-%m-%d'))
            diff_days = aware_date - item.date # 时间相等
            if kdata[0] == item.code and diff_days == 0:
                return True
        return False
        
    def _get_stock_kdata(self, code):
        rs = baostock.query_history_k_data(code, "code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM,date")
        result = list()
        #  获取所有已经存在的对应code的数据
        _k_exists = StockKData.objects.filter(code=code)
        while (rs.error_code == '0') & rs.next():
            kdata = rs.get_row_data()
            print(kdata)
            if not self._compare_stock_date(kdata, _k_exists):
                result.append(
                    StockKData(
                        code=kdata[0],
                        close=Decimal(kdata[1]) if kdata[1] else Decimal(0),
                        peTTM=Decimal(kdata[2]) if kdata[2] else Decimal(0),
                        pbMRQ=Decimal(kdata[3]) if kdata[3] else Decimal(0),
                        psTTM=Decimal(kdata[4]) if kdata[4] else Decimal(0),
                        pcfNcfTTM=Decimal(kdata[5]) if kdata[5] else Decimal(0),
                        date=timezone.make_aware(datetime.datetime.strptime(kdata[6], '%Y-%m-%d'))
                    ))
        return result
    
    def _batch_insert(self, result):
        return StockKData.objects.bulk_create(result)
        
    def get(self, request):
        return self.update()
    
    def _filter_exist_stock_kdata(self):
        '''
            过滤已经存在的kdata数据（kdata，自定义用来描述市盈率相关指标）
        '''
        stockSet = self._query_all_stock()
        result = []
        max_count = 0
        for item in stockSet:
            # DEBUG CODE START
            max_count += 1
            if max_count > 10:
                break
            # DEBUG CODE END
            new_data = self._get_stock_kdata(item.code)
            result.extend(new_data)
        return result
    
    def _query_all_stock(self):
        '''
            返回所有股票代码
        '''
        return StockInfoBase.objects.all()
    
    def update(self):
        result = self._filter_exist_stock_kdata()
        self._batch_insert(result)
        return HttpResponse("success")
