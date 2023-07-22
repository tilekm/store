from django.contrib import admin

from products.models import Basket, Product, ProductCategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['image', 'name', 'description', ('price', 'quantity'), 'category', 'stripe_product_price_id']
    list_display = ['name', 'price', 'quantity', 'category']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(ProductCategory)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['product', 'quantity', 'created_timestamp']
    readonly_fields = ['created_timestamp']
    extra = 0
