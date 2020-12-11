from django.contrib import admin
from kitstock.models.stock_info_base import StockInfoBase
from kitstock.models.stock_kdata import StockKData

admin.site.register(StockInfoBase, StockKData)