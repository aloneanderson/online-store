from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Product, Purchase, PurchaseReturns

# Register your models here.
admin.site.register(Product)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Purchase)
admin.site.register(PurchaseReturns)