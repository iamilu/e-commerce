from django.contrib import admin
from .models.product import Products
from .models.category import Category
from .models.customer import Customer, Otp
from .models.orders import Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Products,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Otp)


# username = Tanushree, email = tanushree7252@gmail.com, password = 1234
