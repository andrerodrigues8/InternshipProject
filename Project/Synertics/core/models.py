from django.db import models

# Create your models here.

class Trade(models.Model):
    day=models.DateField()
    instrument=models.CharField(max_length=200)
    number_of_orders = models.PositiveIntegerField()
    max_price_of_orders = models.DecimalField(max_digits=20, decimal_places=2)
    min_price_of_orders = models.DecimalField(max_digits=20, decimal_places=2)
    average_price_of_orders = models.DecimalField(max_digits=20, decimal_places=2)
    number_of_quotes = models.PositiveIntegerField()
    number_of_trades = models.PositiveIntegerField()
    average_price_of_trades_vwap = models.DecimalField(max_digits=20, decimal_places=2)
    total_quantity_of_trades = models.PositiveIntegerField()
    start_prices = models.DecimalField(max_digits=20, decimal_places=2)
    fixing_prices = models.DecimalField(max_digits=20, decimal_places=2)
    open_interest = models.PositiveIntegerField()
    def __str__(self):
        return self.instrument
