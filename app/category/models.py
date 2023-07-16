from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='products_image/', null=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
