from django.contrib import admin
from .models import Category, Product, Order, CartItem, AnnualSubscriptionCards, CardItem
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('email',)}),
    )
    list_display = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.

admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class AnnualCardsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price')
    prepopulated_fields = {'slug': ('product_name',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'delivery_address', 'total_price', 'ordered_items_list', 'get_description']
    list_filter = ['user']
    search_fields = ['user__username', 'delivery_address']

    def ordered_items_list(self, obj):
        return obj.ordered_items_list()
    ordered_items_list.short_description = 'Ordered Items'

    def get_description(self, obj):
        return obj.description

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__product_name']


class CardItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__product_name']

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(AnnualSubscriptionCards, AnnualCardsAdmin)
admin.site.register(CardItem, CardItemAdmin)

