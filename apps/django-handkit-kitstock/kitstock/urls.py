from django.conf.urls import url
from django.urls import path

from . import views
from .views import StockKDataView

# app_name = 'django-handkit-kitstock'
urlpatterns = [
    path('stock_base/', views.stock_base_info, name='stock_base'),
    path('stock_kdata/', StockKDataView.as_view(), name='stock_kdata'),
]
