from django.urls import path
from .views import *


urlpatterns = [
    path('product/<int:pk>/', GetProducts.as_view(), name='get_product'),
    path('products/<str:slug>/', ListProducts.as_view(), name='category'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('my-cart/', get_cart, name='cart'),
    path('decrease-quantity-in-order/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('increase-quantity-in-order/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('delete-item-in-order/<int:item_id>/', delete_item, name='delete_item'),
    path('create-order/<int:order_id>/', create_order, name='create_order'),
    path('get-orders-history/<int:user_pk>/', get_orders_history, name='get_orders_history'),

    path('create-category/', create_category, name='create_category'),
    path('delete-category/<int:pk>/', delete_category, name='delete_category'),
    path('categories/', ListCategories.as_view(), name='category_list'),
    path('edit-category/<int:pk>/', edit_category, name='edit_category'),
    path('create-product/', create_product, name='create_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('orders/', get_list_orders, name='order_list'),
    path('change_order_status/<int:order_id>/', change_order_status, name='change_order_status'),
]
