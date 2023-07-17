from django.db import models
# from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from ..category.models import Category
from ..account.models import User


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    capacity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_favorite = models.ManyToManyField(User, related_name='product_is_favorite', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_image/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
