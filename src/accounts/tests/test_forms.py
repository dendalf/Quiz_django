from accounts.forms import UserRegisterForm, UserUpdateForm

from django.test import TestCase


class TestForms(TestCase):
    def setUp(self):
        self.username = 'user_1'
        self.password = '123qwe!@#'
        self.email = 'user_1@test.com'
        self.first_name = 'Test_first'
        self.last_name = 'Test_last'
        self.city = 'Kharkiv'
        self.avatar = 'profile/default.png'

    def test_register_form_valid_data(self):
        form = UserRegisterForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            }
        )

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_update_form_valid_data(self):
        form = UserUpdateForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'city': self.city,
                'avatar': self.avatar
            }
        )

        self.assertTrue(form.is_valid())
