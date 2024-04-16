from django.urls import path
from .views import *


urlpatterns = [
    path('product/<int:pk>/', GetProducts.as_view(), name='get_product'),
    path('products/<str:slug>/', ListProducts.as_view(), name='category'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('my-cart/', get_cart, name='cart'),
    path('decrease-quantity/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('increase-quantity/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('create-order/<int:order_id>/', create_order, name='create_order'),
    path('get-my-orders/', get_my_orders, name='get_my_orders'),
]
