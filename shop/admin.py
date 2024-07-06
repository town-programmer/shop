from django.contrib import admin
from .models import Item, Category, Cart

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')

# Register your models here.
admin.site.register(Item, ItemsAdmin)
admin.site.register(Category)
admin.site.register(Cart)