from django.db import models


class StockKData(models.Model):
    """
    code
    close
    peTTM
    pbMRQ
    psTTM
    pcfNcfTTM
    date
    """
    code = models.CharField(max_length=20)
    close = models.DecimalField(decimal_places=10, max_digits=20)
    peTTM = models.DecimalField(decimal_places=10, max_digits=20)
    pbMRQ = models.DecimalField(decimal_places=10, max_digits=20)
    psTTM = models.DecimalField(decimal_places=10, max_digits=20)
    pcfNcfTTM = models.DecimalField(decimal_places=10, max_digits=20)
    date = models.DateTimeField()
    
    class Meta:
        unique_together = ("code", "date")
    
    def __str__(self):
        return "stock kdate"