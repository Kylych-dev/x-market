from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=5, max_digits=2)