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


def entrance_view(request):
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

    return render(request, 'entrance.html', {'form': form})


def viewsrec_view(request):
    users = User.objects.all()  # покупатели
    products = Product.objects.all()  # букеты
    orders = Order.objects.all()  # заказы

    allprice = 0.0  # общая стоимость
    order_prices = {}  # словарь для хранения цен заказов

    for order in orders:
        order_total = 0.0  # общая стоимость для текущего заказа
        for product in order.products.all():
            order_total += float(product.price)
        order_prices[order.id] = order_total  # сохранить цену для заказа
        allprice += order_total  # добавляем к общей стоимости

    context = {
        'users': users,
        'products': products,
        'orders': orders,
        'allprice': f"{allprice:.2f}" if allprice else allprice,
        'order_prices': order_prices,  # передаем словарь с ценами заказов
    }
    return render(request, 'delivery/viewsrec.html', context)
