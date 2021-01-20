import json
import logging

import baostock
import pandas
from django.http import HttpResponse
from django.views import View


class QueryCashFlowView(View):
    logger = logging.getLogger(__name__)
    
    def post(self, request):
        '''
            quarter: 为空--""，默认查当前季度
        '''
        if request.body:
            msg = json.loads(request.body)
            # 查询季频估值指标盈利能力
            profit_list = []
            rs_profit = baostock.query_cash_flow_data(code=msg["code"], year=msg["year"], quarter=msg["quarter"])
            while (rs_profit.error_code == '0') & rs_profit.next():
                profit_list.append(rs_profit.get_row_data())
            result_profit = pandas.DataFrame(profit_list, columns=rs_profit.fields)
            response = result_profit.to_json(orient="records")
            print(response)
            return HttpResponse(json.dumps(response))
        else:
            result = {"code": -1, "msg": "fail"}
            return HttpResponse(result)


