from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    """
    Test suite for ZENZEE Custom User Model.
    Verifies creation of regular users and superusers with phone numbers and profile fields.
    """

    def test_create_user(self):
        user = User.objects.create_user(
            username='arman_fashion',
            email='arman@zenzee.in',
            password='SecurePassword123!',
            phone_number='+919876543210',
            bio='Founder & CTO of ZENZEE'
        )
        self.assertEqual(user.username, 'arman_fashion')
        self.assertEqual(user.email, 'arman@zenzee.in')
        self.assertEqual(user.phone_number, '+919876543210')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), 'arman_fashion (arman@zenzee.in)')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='zenzee_admin',
            email='admin@zenzee.in',
            password='AdminPassword123!'
        )
        self.assertEqual(admin_user.username, 'zenzee_admin')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AccountViewTests(TestCase):
    """
    Test HTTP endpoints for registration, login, and profile.
    """

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_status_code(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirects_anonymous_user(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_order_payment_method_field_exists(self):
        from orders.models import Order
        self.assertTrue(hasattr(Order, 'payment_method'))

    def test_ai_query_api_returns_response(self):
        response = self.client.post('/ai/api/query/', {'prompt': 'oversized hoodie under 1500'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)

    def test_checkout_page_renders_without_template_error(self):
        response = self.client.get('/orders/checkout/')
        self.assertIn(response.status_code, [200, 302])

