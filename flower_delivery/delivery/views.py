from .models import User, Product, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# from django.contrib.auth import authenticate
from .models import User
from .forms import UserRegistrationForm, LoginByEmailForm, LoginForm, DeliveryAddressForm
import pytz


# Функция для отображения главной страницы
def deliver_view(request):
    # Преобразуем время в локальный часовой пояс
    local_time = timezone.now().astimezone(pytz.timezone('Europe/Moscow')).strftime('%H:%M')

    try:  # Пытаемся получить имя пользователя из сессии
        name = request.session['user']
    except:
        name = None
    # Контекст для передачи в шаблон
    context = {'user': name, 'current_time': local_time}
    # Отображение шаблона
    return render(request, 'delivery/deliver.html', context)


# Функция для отображения страницы регистрации
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


# Функция для отображения страницы входа
def entrance_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            request.session['email'] = email
            request.session['user'] = user.name  # Измените на `user.username`, если нужно
            messages.success(request, f'{user.name}, Вы успешно вошли в систему!')
            return redirect('catalog')
    else:
        form = LoginForm()  # Инициализация формы
    return render(request, 'delivery/entrance.html', {'form': form})


# Функция для отображения страницы просмотра записей базы данных
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
    request.session.pop('selected_products', None)
    return redirect('deliver')  # перенаправление на домашнюю страницу


# Функция для отображения страницы каталога букетов
def catalog_view(request):
    try:
        name = request.session['user']
    except:
        name = None

    products = Product.objects.all()  # Получаем все продукты
    user = name

    if name and request.method == 'POST':
        # Получаем список выбранных продуктов
        selected_products = request.POST.getlist('selected_products')
        request.session['selected_products'] = selected_products  # Сохраняем в сессии
        return redirect('order')  # Перенаправление на страницу заказа
    context = {'products': products, 'user': user}
    return render(request, 'delivery/catalog.html', context)

# def order_view(request):
#     selected_products = request.session.get('selected_products', [])
#     print("Сохраненные продукты в сессии:", selected_products)  # Вывод в консоль для отладки
#     context = {'selected_products': selected_products}
#     return render(request, 'delivery/order.html', context)  # Измените на правильный шаблон для заказа
#


# Функция для отображения страницы заказа
def order_view(request):
    # Получаем данные из сессии
    email = request.session.get('email')
    user_name = request.session.get('user')
    selected_products_titles = request.session.get('selected_products', [])

    # Находим пользователя по email
    user = User.objects.filter(email=email).first()

    # Получаем продукты по названиям
    selected_products = Product.objects.filter(title__in=selected_products_titles)

    # Подсчитываем общую сумму заказа
    total_price = sum(product.price for product in selected_products)

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            # Здесь можно создать заказ и сохранить его в БД
            order = Order.objects.create(user=user)
            order.products.set(selected_products)
            order.save()
            # Перенаправление на страницу доставки с данными после создания заказа
            return render(request, 'delivery/deliver.html', {
                'address': address,
                'total_price': total_price
            })
    else:
        form = DeliveryAddressForm()
    # переход на страницу заказа с данными
    return render(request, 'delivery/order.html', {
        'user_name': user_name,
        'selected_products': selected_products,
        'total_price': total_price,
        'form': form
    })
