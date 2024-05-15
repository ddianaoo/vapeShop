from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderDetail, STATUS_CHOICES
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from vapeshop.decorators import custom_login_required, staff_login_required
from .forms import CreateCategoryForm, CreateProductForm, EditProductForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta


STATUS_FILTERS = (
    ('Всі', 'all'),
    ('За останній місяць', 'last_month'),
    ('За останні три місяці', 'last_3_months')
)


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
    return redirect('get_orders_history', request.user.pk)


@login_required
def get_orders_history(request, user_pk):
    if request.user.pk == user_pk or request.user.is_staff:
        orders = Order.objects.filter(user__pk=user_pk).exclude(status=0)
        order_pars = dict()
        for order in orders:
            order_details = OrderDetail.objects.filter(order=order)
            order_pars[order] = order_details
        return render(request, "orders/orders_history.html", {'order_pars': order_pars})
    else:
        messages.error(request, 'Ви не маєте такого права')
        return redirect('home')


#for staff
@staff_login_required
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


@method_decorator(staff_login_required, name='dispatch')
class ListCategories(ListView):
    context_object_name = 'categories'
    paginate_by = 6
    model = Category
    template_name = 'for_staff/category_list.html'


@staff_login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    return redirect('category_list')


@staff_login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категорію успішно відредаговано!')
            return redirect('category_list')
    else:
        form = CreateCategoryForm(instance=category)
    return render(request, 'for_staff/edit_item.html',
                  {'form': form, 'title': 'Редагування категорії'})


@staff_login_required
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


@staff_login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Товар успішно видалено!')
    return redirect('home')


@staff_login_required
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
    return render(request, 'for_staff/edit_item.html',
                  {'form': form, 'title': 'Редагування товару'})


@staff_login_required
def get_list_orders(request):
    queryset = Order.objects.all().order_by('status')

    filter_option = request.GET.get('filter')
    if filter_option == 'last_month':
        start_date = datetime.now() - timedelta(days=30)
        queryset = queryset.filter(created_at__gte=start_date)
    elif filter_option == 'last_3_months':
        start_date = datetime.now() - timedelta(days=90)
        queryset = queryset.filter(created_at__gte=start_date)

    return render(request, 'for_staff/orders.html',
                  {'orders': queryset,
                   'STATUS_CHOICES': STATUS_CHOICES[1:],
                   'STATUS_FILTERS': STATUS_FILTERS})


@staff_login_required
def change_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            if int(order.status) == 1 and int(new_status) > 1:
                for detail in order.orderdetail_set.all():
                    detail.product.stock_quantity -= detail.quantity
                    detail.product.save()
            order.status = new_status
            order.save()
            messages.success(request, 'Статус замовлення успішно змінено.')
        except Order.DoesNotExist:
            messages.error(request, 'Замовлення не знайдено.')
    return redirect('order_list')

