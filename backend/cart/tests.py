from decimal import Decimal
from django.test import TestCase
from products.models import Category, Product, Size, ProductSize
from cart.models import Cart, CartItem


class CartUnitTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Streetwear', slug='streetwear')
        self.product = Product.objects.create(
            name='Test Graphic Tee',
            slug='test-graphic-tee',
            category=self.category,
            description='Test tee',
            price=Decimal('1499.00'),
            is_available=True,
        )
        self.size = Size.objects.create(name='Medium', code='M')
        ProductSize.objects.create(product=self.product, size=self.size, stock_quantity=10)

    def test_cart_add_default_size_fallback(self):
        response = self.client.post(f'/cart/add/{self.product.id}/', follow=True)
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.filter(session_key=self.client.session.session_key).first()
        self.assertIsNotNone(cart)
        item = cart.items.first()
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.size, self.size)

    def test_cart_quantity_update_increase_and_decrease(self):
        self.client.post(f'/cart/add/{self.product.id}/', follow=True)
        cart = Cart.objects.filter(session_key=self.client.session.session_key).first()
        item = cart.items.first()

        # Increase quantity
        self.client.get(f'/cart/update/{item.id}/?action=increase')
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

        # Decrease quantity
        self.client.get(f'/cart/update/{item.id}/?action=decrease')
        item.refresh_from_db()
        self.assertEqual(item.quantity, 1)
