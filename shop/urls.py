from django.urls import path
from .views import *


urlpatterns = [
    # path('zhydkosti/', ZhydkostiListView.as_view(), name='zhydkosti'),
    # path('podsystems/', PodsystemsListView.as_view(), name='podsystems'),
    # path('odnorazki/', OdnorazkiListView.as_view(), name='odnorazki'),
    # path('components/', ComponentsListView.as_view(), name='components'),
    path('product/<int:pk>/', GetProducts.as_view(), name='get_product'),
    path('products/<str:slug>/', ListProducts.as_view(), name='category'),
]
