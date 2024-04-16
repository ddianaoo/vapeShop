from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderDetail
from django.views.generic import View, ListView, DetailView
from django.contrib import messages


class ListProducts(ListView):
    context_object_name = 'products'
    paginate_by = 8
    template_name = 'products/products_list.html'

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetProducts(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'


#Orders
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status=0)
    order_detail, created = OrderDetail.objects.get_or_create(order=order, product=product)
    messages.success(request, 'Товар додано до кошику!')
    return redirect("cart")


def get_cart(request):
    order = Order.objects.get(user=request.user, status=0)
    order_details = OrderDetail.objects.filter(order=order)
    return render(request, "orders/cart.html", {'cart_items': order_details})


def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.quantity -= 1
    if item.quantity < 1:
        item.delete()
    else:
        item.save()
    return redirect('cart')


def increase_quantity(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def delete_item(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.delete()
    return redirect('cart')
