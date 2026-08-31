from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Акаунт успішно створено! Вітаємо, {user.first_name}.")
            return redirect('user_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            name_to_show = user.first_name or user.email
            messages.success(request, f"З поверненням, {name_to_show}!")
            return redirect('user_list')
        else:
            messages.error(request, "Невірний email або пароль.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Ви успішно вийшли з системи.")
    return redirect('login')


@login_required(login_url='login')
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users.html', {'users': users})