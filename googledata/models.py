from django.db import models


class NumbersModel(models.Model):
    order = models.IntegerField('номер заказа', unique=True, blank=False)
    cost_usd = models.DecimalField('стоимость $', max_digits=6, decimal_places=2)
    cost_rub = models.DecimalField('стоимость руб.', max_digits=12, decimal_places=2)
    delivery_date = models.DateField('срок поставки', auto_now=False, auto_now_add=False)

