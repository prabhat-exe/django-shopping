from django.contrib import admin
from .models import Category, Customers, Product,Cart

# Register your models here.
class all_productAdmin(admin.ModelAdmin):
    list_display = ('id','pname', 'price')  # Customize displayed fields in the admin list view

class cartAdmin(admin.ModelAdmin):
    list_display=('id','product','cus_id','quantity')

admin.site.register(Category)  # Register Category model
admin.site.register(Customers)  # Register Customers model
admin.site.register(Product, all_productAdmin)  # Register Product model with custom admin options
admin.site.register(Cart,cartAdmin)