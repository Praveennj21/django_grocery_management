from django.contrib import admin
from .models import Product, Bill, TotalAmount, User, Shop, Employee

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop_id', 'owner', 'manager', 'license_no')
    ordering = ('name',)
    search_fields = ('shop_id',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'emp_id', 'shop',)
    ordering = ('name',)
    search_fields = ('name',)


