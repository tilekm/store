from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User

# Create your tests here.


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'test123',
            'email': 'test@test.test',
            'password1': '12345678pP',
            'password2': '12345678pP'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')

    def test_user_registration_success(self):
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

    def test_user_registration_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')


class UserLoginTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:login')
        self.data = {
            'username': 'test',
            'password': '12345678pP'
        }

    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(response.context_data['title'], 'Store - Авторизация')

    def test_user_login_post_success(self):
        User.objects.create_user(username=self.data['username'], password=self.data['password'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))

    def test_user_login_post_error(self):
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,
                            'Пожалуйста, введите правильные имя пользователя и пароль. '
                            'Оба поля могут быть чувствительны к регистру.')
