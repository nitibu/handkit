import datetime
import logging
import string
from decimal import Decimal

import baostock
from baostock.data.resultset import ResultData
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from django.views import View

# 独立app逻辑
from kitstock.models import StockKData, StockInfoBase


class StockKDataView(View):
    logger = logging.getLogger(__name__)
    # lg = baostock.login()
    
    # def __del__(self):
    #     baostock.logout()
    
    @classmethod
    def is_exist(self, kdata: ResultData, start_date: str) -> bool:
        '''
            kdata: baostock.query_history_k_data返回的数据集
            start_date: 开始查询的时间
            判断ResultData是不是开始时间start_date的数据，是-True
        '''
        aware_date = kdata[6]
        
        if start_date.__eq__(aware_date):
            # print("%s, %s, %s" % (__name__, "aware_date", aware_date))
            # print("%s, %s, %s" % (__name__, "start_date", start_date))
            return True
        return False
    
    def _update_date_range(self, code: string):
        row = StockKData.objects.filter(code=code).order_by("-date").first()
        # 如果没有原始数据存在，直接返回
        if not row:
            start_date = "2015-01-04" # baostock目前能查到的最早数据
        else:
            start_date = row.date.strftime("%Y-%m-%d")
        end_date = timezone.now().strftime("%Y-%m-%d")
        return start_date, end_date
    
    def _get_stock_kdata(self, code:string, update_time: datetime.datetime) -> list:
        '''
            1. 查询数据库现有数据，获取离当日最近日期的数据（判断当日是否是最后一个工作日，是的话，就去下一个工作日作为startDate）, endDate作为截止日期
            2. 根据上一步的startDate和endDate，获取历史数据
            3. 保存获取到的数据到数据库里
        '''
        print("%s, %s, %s" % (__name__, "update_time", update_time.strftime("%Y-%m-%d")))
        print("%s, %s, %s" % (__name__, "now_time", timezone.now().strftime("%Y-%m-%d")))
        if update_time.strftime("%Y-%m-%d") < timezone.now().strftime("%Y-%m-%d"):
            start_date = update_time.strftime("%Y-%m-%d")
            end_date = timezone.now().strftime("%Y-%m-%d")
        else:
            start_date, end_date = self._update_date_range(code)
        # 根据start date 和end date 获取历史数据
        rs = baostock.query_history_k_data(
            code,
            "code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM,date",
            start_date=start_date,
            end_date=end_date)
        result = list()
        while (rs.error_code == '0') & rs.next():
            kdata = rs.get_row_data()
            # 因为取的是数据库中时间离当前最近的一条数据作为start time，所以这条数据不用重新保存
            if self.is_exist(kdata, start_date):
                continue
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
    
    def _batch_insert(self, result: list):
        return StockKData.objects.bulk_create(result)
    
    def get(self, request):
        print("%s, %s, %s" % (__name__, "request", request.get_full_path()))
        return self.update()
        # return self.unique()
    
    def _store_exist_stock_kdata(self):
        '''
            过滤已经存在的kdata数据（kdata，自定义用来描述市盈率相关指标）
        '''
        stockSet = self._query_all_stock()
        for item in stockSet:
            new_data = self._get_stock_kdata(item.code, item.update_time)
            # 有数据才进行插入操作
            if new_data.__len__() > 0:
                print("%s, %s, %s" % (__name__, "code", item.code))
                self._batch_insert(new_data)
            # 更新基础表股票更新时间
            StockInfoBase.objects.filter(code=item.code).update(
                update_time=timezone.now().date())
    
    def _query_all_stock(self):
        '''
            返回所有股票代码
        '''
        return StockInfoBase.objects.all()
    
    def update(self):
        self._store_exist_stock_kdata()
        return HttpResponse("success")
    
    def _delete_repeating_data(self, code:string):
        dataset = StockKData.objects.filter(code=code)
        filter_date = list()
        for item in dataset:
            if item.date not in filter_date:
                filter_date.append(item.date)
                continue
            else:
                StockKData.objects.get(id=item.id).delete()
                
            
    
    def unique(self):
        stockSet = self._query_all_stock()
        for item in stockSet:
            self._delete_repeating_data(item.code)
        return HttpResponse("success")
