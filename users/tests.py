from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Course, Lesson
from users.models import User, Subscription


class UserTestCase(APITestCase):
    """ Тест кейс контроллера UserViewSet. """

    def setUp(self):
        """ Начальный сет-ап с тестовыми данными. """
        self.user1 = User.objects.create(email="admin@gmail.com")
        self.user1.set_password("7777")
        self.user1.save()

        self.user2 = User.objects.create(email="admin777@gmail.com")
        self.user2.set_password("7777")
        self.user2.save()

    def test_user_register(self):
        """ Тестирование получаемых данных для -> users:user-create. """
        url = reverse("users:users-list")
        data = {
            "email": "example@gmail.com",
            "password": "7777"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            User.objects.all().count(), 3
        )

        self.assertEqual(
            response.data['email'], data["email"]
        )

    def test_get_token_for_user(self):
        """ Тестирование получаемых данных для -> users:login. """
        url = reverse("users:login")
        data = {
            "email": "admin@gmail.com",
            "password": "7777"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
        self.assertTrue(response.data['access'])
        self.assertTrue(response.data['refresh'])


    def test_get_token_wrong_password(self):
        """ Тестирование получаемых данных для -> users:login. """
        url = reverse("users:login")
        data = {
            "email": "admin@gmail.com",
            "password": "wrong_pass"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEqual(
            response.json(),
        {'detail': 'No active account found with the given credentials'}
        )