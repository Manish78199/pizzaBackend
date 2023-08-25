from django.contrib import admin
from pizzaapp.models import Product,User,Vendor,Cart
# Register your models here.
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(User)
admin.site.register(Cart)