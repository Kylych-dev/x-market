from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from . import managers


class Order(models.Model):
    STATUS = (
        ('R','received'),
        ('P','posted'),
        ('N','not posted'),
    )

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    # product = models.ForeignKey(
    #     to=models.
    # )


    total_price = models.PositiveIntegerField(default=0)