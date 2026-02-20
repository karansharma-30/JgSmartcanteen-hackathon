from django.contrib import admin
from .models import FoodItem, Cart, Order


# FOOD ADMIN

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'available')

    list_editable = ('price', 'available')

    search_fields = ('name',)

    list_filter = ('available',)



# ORDER ADMIN

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('user', 'food', 'quantity', 'status', 'created_at')

    list_editable = ('status',)

    list_filter = ('status',)

    search_fields = ('user__username', 'food__name')



# CART ADMIN (optional but useful)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ('user', 'food', 'quantity')

    search_fields = ('user__username',)