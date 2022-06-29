from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','desc')
    search_fields = ('name',)

    def set_price_to_zero(self,request,queryset):
        queryset.update(price=0)

    actions = ('set_price_to_zero',)
    list_editable = ('price',)
    

admin.site.register(Product,ProductAdmin)
admin.site.site_header="Buy and Sell Website"