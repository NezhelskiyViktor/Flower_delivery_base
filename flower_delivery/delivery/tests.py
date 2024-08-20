from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Order


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title='Розы', price=100.00)

    def test_product_creation(self):
        self.assertEqual(self.product.title, 'Розы')
        self.assertEqual(self.product.price, 100.00)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Розы')


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser', email='p4VZI@example.com')
        self.product1 = Product.objects.create(title='Розы', price=100.00)
        self.product2 = Product.objects.create(title='Тюльпаны', price=150.00)
        self.order = Order.objects.create(user=self.user)
        self.order.products.add(self.product1, self.product2)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.products.count(), 2)

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Заказ {self.order.id} для покупателя {self.user.name}')

    def test_order_products_relationship(self):
        self.assertIn(self.product1, self.order.products.all())
        self.assertIn(self.product2, self.order.products.all())