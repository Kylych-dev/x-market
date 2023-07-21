from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from app.product.models import Product
from app.utils import choicess

from app.account.models import User


class Order(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(null=True, blank=True)
    pay_price = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, 
                              choices=choicess.ORDER_STATUS, 
                              default='N')
    pay_date = models.DateTimeField()


    @property
    def name(self):
        return f'{self.full_}'

    def __str__(self):
        return str(self.pay_price)


class OrderItems(models.Model):
    order = models.ForeignKey(to=Order, 
                              on_delete=models.CASCADE,
                              related_name='orderitems')
    product = models.ForeignKey(to=Product,
                                on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    invoice_id = models.CharField(max_length=100, null=True)
    

    def __str__(self):
        return self.product.name
    
    def total_price(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        self.total_price()
        return super().save(*args, **kwargs)
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=choicess.PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_id
    