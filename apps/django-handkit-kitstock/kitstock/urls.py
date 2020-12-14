from django.urls import path

from . import views

urlpatterns = [
    path('stock_base/', views.stock_base_info, name='stock_base'),
    path('stock_kdata/', views.StockKDataView.as_view(), name='stock_kdata'),
]
