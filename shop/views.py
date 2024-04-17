from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderDetail, STATUS_CHOICES
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from vapeshop.decorators import custom_login_required
from .forms import CreateCategoryForm, CreateProductForm, EditProductForm


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
@custom_login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(user=request.user, status=0)
    order_detail, created = OrderDetail.objects.get_or_create(order=order, product=product)
    messages.success(request, 'Товар додано до кошику!')
    return redirect("cart")


@custom_login_required
def get_cart(request):
    order, created = Order.objects.get_or_create(user=request.user, status=0)
    order_details = OrderDetail.objects.filter(order=order)
    return render(request, "orders/cart.html", {'order': order, 'cart_items': order_details})


@custom_login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.quantity -= 1
    if item.quantity < 1:
        item.delete()
    else:
        item.save()
    return redirect('cart')


@custom_login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    if item.quantity < item.product.stock_quantity:
        item.quantity += 1
    else:
        messages.error(request, 'Ви обрали максимальну кількість товару, яка є на складі')
    item.save()
    return redirect('cart')


@custom_login_required
def delete_item(request, item_id):
    item = get_object_or_404(OrderDetail, id=item_id)
    item.delete()
    return redirect('cart')


@custom_login_required
def create_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 1
    order.save()
    messages.success(request, 'Ви успішно оформили замовлення!')
    return redirect('home')


@custom_login_required
def get_my_orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status=0)
    order_pars = dict()
    for order in orders:
        order_details = OrderDetail.objects.filter(order=order)
        order_pars[order] = order_details
    return render(request, "orders/orders_history.html", {'order_pars': order_pars, 'STATUS_CHOICES': STATUS_CHOICES })


#for staff
def create_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успішно додано нову категорію!')
            return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = CreateCategoryForm()
    return render(request, 'for_staff/create_category.html', {'form': form})


class ListCategories(ListView):
    context_object_name = 'categories'
    paginate_by = 6
    template_name = 'for_staff/category_list.html'

    def get_queryset(self):
        return Category.objects.all()


def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect('category_list')


def create_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Успішно додано новий товар!')
            return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = CreateProductForm()
    return render(request, 'for_staff/create_product.html', {'form': form})


def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Товар успішно видалено!')
    return redirect('home')


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успішно відредаговано!')
            return redirect('get_product', pk)
    else:
        form = EditProductForm(instance=product)
    return render(request, 'for_staff/edit_product.html', {'form': form})
