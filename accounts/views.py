from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages


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
    return render(request, 'accounts/signup.html', {'form': form})


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
