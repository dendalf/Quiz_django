from django.test import SimpleTestCase
from django.urls import reverse, resolve

from accounts.views import UserRegisterView, user_profile_view, user_activate, user_send_verification, UserLoginView, \
    UserLogoutView


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, user_profile_view)

    def test_send_verification_url_resolves(self):
        url = reverse('accounts:send_verification')
        self.assertEqual(resolve(url).func, user_send_verification)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_activate_user_url_resolves(self):
        url = reverse('accounts:register_activate', kwargs={'sign': 'ioewutrljc3409ur90u43ri3j4'})
        self.assertEqual(resolve(url).func, user_activate)
