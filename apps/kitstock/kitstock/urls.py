from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('stock_base/', views.stock_base_info, name='stock_base'),
    path('stock_kdata/', views.StockKDataView.as_view(), name='stock_kdata'),
    path('queryProfit', views.QueryProfitView.as_view(), name='queryProfit'),
    path('queryOperation', views.QueryOperationView.as_view(), name='queryOperation'),
    path('queryGrowth', views.QueryGrowthView.as_view(), name='queryGrowth'),
    path('queryBalance', views.QueryBalanceView.as_view(), name='queryBalance'),
    path('queryCashFlow', views.QueryCashFlowView.as_view(), name='queryCashFlow'),
]
