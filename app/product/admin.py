from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'buy_price', 'sell_price', 'category']
    search_fields = ['title', 'category']
