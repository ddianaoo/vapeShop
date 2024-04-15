from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category__title__contains=self.category_filter)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category_filter
        return context


class ZhydkostiListView(ProductListView):
    category_filter = 'рідини'


class PodsystemsListView(ProductListView):
    category_filter = 'POD-системи'


class OdnorazkiListView(ProductListView):
    category_filter = 'одноразові сигарети'


class ComponentsListView(ProductListView):
    category_filter = 'картриджі'


class GetProducts(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'



