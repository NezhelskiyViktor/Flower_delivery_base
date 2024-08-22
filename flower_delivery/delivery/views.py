import pytz
from .models import User, Product, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import User
from .forms import UserRegistrationForm, LoginByEmailForm, LoginForm, DeliveryAddressForm
from .telebot.message_to_bot import send_message
from datetime import datetime

TIME = (8, 23)

# Функция для отображения главной страницы
def deliver_view(request):
    global TIME
    time_open = TIME[0]
    time_close = TIME[1]

    local_time = timezone.now().astimezone(pytz.timezone('Europe/Moscow'))

    # Установим время начала и окончания работы
    start_time = local_time.replace(hour=time_open, minute=0, second=0, microsecond=0)
    end_time = local_time.replace(hour=time_close, minute=0, second=0, microsecond=0)

    is_open = start_time <= local_time <= end_time

    try:
        buyer = request.session['buyer']
    except KeyError:
        buyer = None

    context = {
        'user': buyer,
        'current_time': local_time.strftime('%H:%M'),
        'open': str(time_open),
        'close': str(time_close),
        'is_open': is_open  # Передаем информацию о доступности доставки
    }

    return render(request, 'delivery/deliver.html', context)


# Функция для отображения страницы регистрации
def registration_view(request):
    if request.method == 'POST':  # Обработка POST-запроса
        form = UserRegistrationForm(request.POST)  # Инициализация формы
        if form.is_valid():  # Проверка формы
            form.save()  # Сохранение формы
            email = form.cleaned_data['email']  # Получить email из формы
            buyer = get_object_or_404(User, email=email)  # Поиск пользователя по email
            request.session['email'] = email  # запомнить email в сессии
            request.session['buyer'] = buyer.name  # запомнить имя пользователя в сессии
            # messages.success(request, 'Пользователь успешно зарегистрирован!')
            return redirect('catalog')  # Перенаправление на страницу каталога
    else:
        form = UserRegistrationForm()  # Инициализация формы
    # Отображение формы
    return render(request, 'delivery/registration.html', {'form': form})


# Функция для отображения страницы входа
def entrance_view(request):
    if request.method == 'POST':  # Обработка POST-запроса
        form = LoginForm(request.POST)  # Инициализация формы
        if form.is_valid():
            email = form.cleaned_data['email']  # Получить email из формы
            buyer = get_object_or_404(User, email=email)  # Поиск пользователя по email
            request.session['email'] = email  # запомнить email в сессии
            request.session['buyer'] = buyer.name  # запомнить имя пользователя в сессии
            # messages.success(request, f'{buyer.name}, Вы успешно вошли в систему!')
            return redirect('catalog')  # Перенаправление на страницу каталога
    else:
        form = LoginForm()  # Инициализация формы

    # Отображение формы
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
    request.session.pop('buyer', None)
    request.session.pop('selected_products', None)
    return redirect('deliver')  # перенаправление на домашнюю страницу


# Функция для отображения страницы каталога букетов
def catalog_view(request):
    try:
        buyer = request.session['buyer']
    except:
        buyer = None

    products = Product.objects.all()  # Получаем все продукты
    user = buyer

    if buyer and request.method == 'POST':
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
    buyer = request.session.get('buyer')
    selected_products_titles = request.session.get('selected_products', [])

    # Находим пользователя по email чтобы записать заказ в БД
    user = User.objects.filter(email=email).first()

    # Получаем продукты по названиям
    selected_products = Product.objects.filter(title__in=selected_products_titles)

    # Подсчитываем общую сумму заказа
    total_price = sum(product.price for product in selected_products)

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            text = form.cleaned_data['text']
            formatted_date_time = datetime.now().strftime("%H:%M %d.%m.%Y")

            # Здесь можно создать заказ и сохранить его в БД
            order = Order.objects.create(user=user)
            order.products.set(selected_products)
            order.save()
            text_for_bot = (f'{formatted_date_time} |{order} | Список букетов: {selected_products_titles} | '
                   f'Сумма заказа: {total_price}₽ | Адрес доставки: {address} | ')

            if text != '':
                text_for_bot += f'{text}'

            send_message(text_for_bot)

            local_time = timezone.now().astimezone(pytz.timezone('Europe/Moscow'))
            global TIME
            # Перенаправление на страницу доставки с данными после создания заказа
            return render(request, 'delivery/deliver.html', {
                'user': buyer,
                'current_time': local_time.strftime('%H:%M'),
                'open': str(TIME[0]),
                'close': str(TIME[1]),
                'is_open': True  # Передаем информацию о доступности доставки
            })
    else:
        form = DeliveryAddressForm()
    # переход на страницу заказа с данными
    return render(request, 'delivery/order.html', {
        'user_name': buyer,
        'selected_products': selected_products,
        'total_price': total_price,
        'form': form
    })
