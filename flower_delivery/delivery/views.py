from .models import User, Product, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User
from .forms import UserRegistrationForm, LoginByEmailForm
import time


def deliver_view(request):  #
    try:
        name = request.session['user']
    except:
        name = ''
    context = {'user': name}  # Контекст для передачи в шаблон
    # Отображение шаблона
    return render(request, 'delivery/deliver.html', context)


def registration_view(request):
    if request.method == 'POST':  # Обработка POST-запроса
        form = UserRegistrationForm(request.POST)  # Инициализация формы
        if form.is_valid():  # Проверка формы
            form.save()  # Сохранение формы
            messages.success(request, 'Пользователь успешно зарегистрирован!')
            return redirect('registration')  # Перенаправление на страницу регистрации
    else:
        form = UserRegistrationForm()  # Инициализация формы
    # Отображение формы
    return render(request, 'delivery/registration.html', {'form': form})


def entrance_view(request):
    if request.method == 'POST':  # Обработка POST-запроса
        form = LoginByEmailForm(request.POST)  # Инициализация формы
        if form.is_valid():  # Проверка формы
            email = form.cleaned_data['email']  # Получение значения электронной почты
            # Проверяем, существует ли пользователь с такой почтой
            if User.objects.filter(email=email).exists():
                # Запоминаем email в сессионном хранилище
                request.session['email'] = form.cleaned_data['email']
                user = get_object_or_404(User, email=email)
                request.session['user'] = user.name

                messages.success(request, f'{user.name}, Вы успешно вошли в систему!')
                # return redirect('deliver')  # Перенаправление на домашнюю страницу
            else:
                messages.error(request, 'Пользователь с такой электронной почтой не найден.')
    else:
        form = LoginByEmailForm()
    return render(request, 'delivery/entrance.html', {'form': form})


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


def exit_view(request):
    # Очистить конкретные данные
    request.session.pop('email', None)
    request.session.pop('user', None)

    return redirect('deliver')  # перенаправление на домашнюю страницу