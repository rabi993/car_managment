from django.contrib import admin
from .models import UserBankAccount, UserAddress, BuyItem, Product
# Register your models here.

admin.site.register(UserBankAccount)
admin.site.register(UserAddress)
admin.site.register(BuyItem)
admin.site.register(Product)

