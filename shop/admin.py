from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'featured', 'is_draft', 'date']
    list_filter = ['featured', 'is_draft', 'category']
    list_editable = ['featured', 'is_draft']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
