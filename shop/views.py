from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderDetail, STATUS_CHOICES
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
    order, created = Order.objects.get_or_create(user=request.user, status=0)
    order_details = OrderDetail.objects.filter(order=order)
    return render(request, "orders/cart.html", {'order': order, 'cart_items': order_details})


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
    print(item.product.stock_quantity)
    if item.quantity < item.product.stock_quantity:
        item.quantity += 1
    else:
        messages.error(request, 'Ви обрали максимальну кількість товару, яка є на складі')
    item.save()
    return redirect('cart')


def delete_item(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.delete()
    return redirect('cart')


def create_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 1
    order.save()
    messages.success(request, 'Ви успішно оформили замовлення!')
    return redirect('home')


def get_my_orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status=0)
    order_pars = dict()
    for order in orders:
        order_details = OrderDetail.objects.filter(order=order)
        order_pars[order] = order_details
    return render(request, "orders/orders_history.html", {'order_pars': order_pars, 'STATUS_CHOICES': STATUS_CHOICES })
