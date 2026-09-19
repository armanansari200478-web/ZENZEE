from decimal import Decimal

from django.test import TestCase

from .models import Brand, Category, Product


class ProductPricingTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Streetwear', slug='streetwear')
        self.brand = Brand.objects.create(name='ZENZEE', slug='zenzee')
        self.product = Product.objects.create(
            name='Test Hoodie',
            slug='test-hoodie',
            category=self.category,
            brand=self.brand,
            description='A test product for pricing validation.',
            price=Decimal('1999.00'),
            discount_price=Decimal('1299.00'),
            is_available=True,
        )

    def test_effective_price_uses_discount_when_lower(self):
        self.assertEqual(self.product.get_effective_price(), Decimal('1299.00'))

    def test_discount_amount_is_calculated_from_price_and_discount_price(self):
        self.assertEqual(self.product.get_discount_amount(), Decimal('700.00'))

    def test_discount_percentage_is_calculated_correctly(self):
        self.assertEqual(self.product.get_discount_percentage(), 35)


class ProductListViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Oversized', slug='oversized')
        self.product = Product.objects.create(
            name='Oversized Heavyweight Hoodie',
            slug='oversized-heavyweight-hoodie',
            category=self.category,
            description='Test description',
            price=Decimal('2999.00'),
            is_available=True,
        )

    def test_category_filter_by_slug_and_name(self):
        response = self.client.get('/products/', {'category': 'oversized'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product, response.context['products'])

    def test_sort_selection_retained_in_context(self):
        response = self.client.get('/products/', {'sort': 'price_low'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_sort'], 'price_low')
