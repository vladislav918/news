import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")

import django

django.setup()
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import authenticate
from .token import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class RegisterTestCase(TestCase):
    def test_get(self):
        activate_url = reverse('register')
        response = self.client.get(activate_url)
        self.assertEqual(response.status_code, 200)

    def test_post_ok(self):
        email = 'test_email@mail.ru'

        payload = {
            'username': 'username',
            'email': email,
            'password1': 'L;fyuj123123',
            'password2': 'L;fyuj123123',
        }

        response = self.client.post(reverse('register'), data=payload)

        user = User.objects.get(email=email)

        self.assertEqual(user.email, email)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_authenticated)


class ChangeProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com',
                                             password='testpassword123', first_name='Dima', last_name='Dimov')
        self.client.login(username='testuser@example.com', password='testpassword123')
        self.change_profile_url = reverse('change_profile', args=[self.user.id])
        self.valid_data = {
            'first_name': 'Dima',
            'last_name': 'Dimov',
            'email': 'testuser@example.com',
            'avatar': SimpleUploadedFile("avatar.jpg", b'file_content', content_type='image/jpeg')
        }
        self.invalid_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'avatar': ''
        }

    def test_change_profile_view(self):
        response = self.client.get(self.change_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_change_profile_valid_data(self):
        response = self.client.post(self.change_profile_url, data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, self.valid_data['email'])
        self.assertIsNotNone(self.user.avatar)
        self.assertEqual(self.user.first_name, self.valid_data['first_name'])
        self.assertEqual(self.user.last_name, self.valid_data['last_name'])

    def test_change_profile_invalid_data(self):
        response = self.client.post(self.change_profile_url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com',
                                             password='testpassword123')
        self.login_url = reverse('login')
        self.valid_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.invalid_data = {
            'username': '1',
            'password': '2',
        }

    def test_login_user_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_user_valid_data(self):
        response = self.client.post(self.login_url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_user_invalid_data(self):
        response = self.client.post(self.login_url, data=self.invalid_data)
        self.assertEqual(response.status_code, 200)


class ActivateAccountTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com',
                                             password='testpassword123')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        self.activate_url = reverse('activate', kwargs={'uidb64': self.uidb64, 'token': self.token})
        self.invalid_uidb64 = urlsafe_base64_encode(force_bytes(999))
        self.invalid_token = account_activation_token.make_token(User())

    def test_activate_account_valid_data(self):
        response = self.client.get(self.activate_url)
        self.assertEqual(response.status_code, 302)
        user = authenticate(username='testuser@example.com', password='testpassword123')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_active)

    def test_activate_account_invalid_uidb64(self):
        invalid_activate_url = reverse('activate', kwargs={'uidb64': self.invalid_uidb64, 'token': self.token})
        response = self.client.get(invalid_activate_url)
        self.assertEqual(response.status_code, 200)

    def test_activate_account_invalid_token(self):
        invalid_activate_url = reverse('activate', kwargs={'uidb64': self.uidb64, 'token': self.invalid_token})
        response = self.client.get(invalid_activate_url)
        self.assertEqual(response.status_code, 200)
