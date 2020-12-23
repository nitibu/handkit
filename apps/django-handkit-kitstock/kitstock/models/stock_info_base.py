import datetime

from django.db import models
from django.utils import timezone


class StockInfoBase(models.Model):
    code = models.CharField(max_length=20)
    status = models.IntegerField()
    name = models.CharField(max_length=50)
    update_time = models.DateTimeField(
        default=timezone.make_aware(datetime.datetime.strptime("2015-01-04", '%Y-%m-%d')))
   
    def __str__(self):
        return self.name
