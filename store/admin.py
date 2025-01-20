from django.contrib import admin
from .models import (User, category, Products, subcategory,carousel,special_offer,featured_products, Product_image,
                     CartItem, Order, Cart,Review,ShippingDetails, OrderHistory,NewsletterSubscription
                     )

admin.site.register(User)
admin.site.register(category)
admin.site.register(Product_image)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(ShippingDetails)

admin.site.register(OrderHistory)
admin.site.register(NewsletterSubscription)



class subcategoryAdmin(admin.ModelAdmin):  # Use the regular ModelAdmin
  search_fields=['sub_category_name']
  prepopulated_fields = {'slug': ('sub_category_name',)}
  
admin.site.register(subcategory)


  
  
class ProductAdmin(admin.ModelAdmin):  # Use the regular ModelAdmin
  list_display = ['__str__','published', 'updated']
  search_fields=['name']
  prepopulated_fields = {'slug': ('name',)}
  
admin.site.register(Products,ProductAdmin)

admin.site.register(carousel)

admin.site.register(special_offer)
admin.site.register(featured_products)
  
 


