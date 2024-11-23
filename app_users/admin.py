from django.contrib import admin

from .models import UserModel, Cart
# Register your models here.

admin.site.register(UserModel)
admin.site.register(Cart)