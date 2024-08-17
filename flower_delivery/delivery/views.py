from .models import User, Product, Order
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from .forms import UserRegistrationForm, LoginForm


def deliver_view(request):
    users = User.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()

    context = {
        'users': users,
        'products': products,
        'orders': orders,
    }
    return render(request, 'delivery/deliver.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь успешно зарегистрирован!')
            return redirect('registration')
    else:
        form = UserRegistrationForm()

    return render(request, 'delivery/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['name']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('registration', user.id)
            else:
                form.add_error(None, 'Неверная электронная почта или пароль.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})