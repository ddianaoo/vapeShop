from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import View, ListView, DetailView
from .models import CustomUser
from vapeshop.decorators import custom_login_required, staff_login_required
from django.utils.decorators import method_decorator


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # registration only
            form.save()
            messages.success(request, 'Успішна реєстрація!')
            return redirect('signin')

            # registration and login
            # user = form.save()
            # login(request, user)
            # messages.success(request, 'Успішна реєстрація! Ви увійшли!')
            # return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form, 'title': 'Реєстрація'})


def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Ви увійшли')
            return redirect('home')
        else:
            error = {}
            for field in form.errors:
                error[field] = form.errors[field].as_text()
            messages.error(request, *[e[1:] for e in error.values()])
            form = UserLoginForm()
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')


@method_decorator(staff_login_required, name='dispatch')
class ListUsers(ListView):
    context_object_name = 'users'
    paginate_by = 10
    model = CustomUser
    template_name = 'accounts/user_list.html'


@staff_login_required
def add_assistant(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = False
            user.save()
            messages.success(request, 'Ви додали помічника!')
            return redirect('user_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html',
                  {'form': form, 'title': 'Додати помічника'})


@custom_login_required
def edit_user(request):
    user = get_object_or_404(CustomUser, pk=request.user.pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваші дані успішно відредаговано!')
            return redirect('home')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'for_staff/edit_item.html',
                  {'form': form, 'title': 'Редагування профілю'})


@custom_login_required
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    return redirect('signout')
