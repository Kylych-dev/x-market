from django.contrib import admin

from .models import Category

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    search_fields = ['name']

