from django.contrib import admin

from .models import (
    Customer,
    Products,
    Cart,
    Orderplaced,
    UserLogRe
)

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Products)
admin.site.register(Orderplaced)
admin.site.register(UserLogRe)
   

# @admin.register(Customer)
# class CustomerModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','name','locality','city','zipcode','state']

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ['id','title','selling_price','discounted_price','description','brand','category','product_img']

# @admin.register(Cart)
# class CartModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','product','quantity']

# @admin.register(Orderplaced)
# class OrderPlaceModelAdmin(admin.ModelAdmin):
#     list_display = ['id','user','customer','product','quantity','order_date','status']