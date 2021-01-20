import baostock
from django.apps import AppConfig


class KitstockConfig(AppConfig):
    name = 'kitstock'

    def ready(self):
        baostock.login()