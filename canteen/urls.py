from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # CART
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart'),

    path('remove/<int:id>/', views.remove_from_cart, name='remove'),

    # ORDER
    path('place-order/', views.place_order, name='place_order'),

    path('orders/', views.orders_view, name='orders'),

    # AUTH
    path('register/', views.register, name='register'),

    path('verify/', views.verify, name='verify'),

]