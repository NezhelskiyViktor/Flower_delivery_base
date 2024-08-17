from django.db import models
from django.urls import reverse  # Для генерации URL-адресов путем изменения шаблонов URL- перебором в обратном проядке.
from django.db.models import UniqueConstraint  # Для добавления уникальных ограничений
from django.db.models.functions import Lower  # Для добавления уникальных ограничений

# Create your models here.


class User(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Product(models.Model):
    title = models.CharField(verbose_name='Букет', max_length=255)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name='Букеты', related_name='orders')

    def __str__(self):
        return f"Заказ {self.id} для покупателя {self.user.name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
