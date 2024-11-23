from django.contrib import admin
from django.contrib.auth.models import Group


from .models import Product,Categories

admin.site.register(Product)
admin.site.register(Categories)