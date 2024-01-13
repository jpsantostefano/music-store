from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Profile, Product, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)