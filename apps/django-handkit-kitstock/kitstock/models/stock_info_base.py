from django.db import models


class StockInfoBase(models.Model):
    code = models.CharField(max_length=20)
    status = models.IntegerField()
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
