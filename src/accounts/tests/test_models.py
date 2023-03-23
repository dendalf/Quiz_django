from accounts.models import User, avatar_save

from django.test import TestCase


class TestModels(TestCase):
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='123qwe!@#',
            email='user_1@test.com',
            first_name='Test'
        )

    def setUp(self):
        self.user = User.objects.get(username=self.username)

    def test_avatar_label_is_correct(self):
        meta = self.user._meta.get_field('avatar')
        self.assertEqual(meta.verbose_name, 'avatar')
        self.assertEqual(meta.upload_to, avatar_save)
        self.assertTrue(meta.default, 'profile/default.png')

    def test_city(self):
        meta = self.user._meta.get_field('city')
        self.assertEqual(meta.max_length, 50)
        self.assertTrue(meta.null)
        self.assertTrue(meta.blank)

    def test_birthdate(self):
        meta = self.user._meta.get_field('birthdate')
        self.assertTrue(meta.null)
        self.assertTrue(meta.blank)

    def test_convert_user_to_str(self):
        self.assertEqual(str(self.user), self.username)