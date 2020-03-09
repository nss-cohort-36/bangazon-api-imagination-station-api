from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

class TestAuth(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

    @skip
    def test_login(self):

        user_to_login = {
            "username": "testuser",
            "password": "foobar" 
        }

        response = self.client.post(
            reverse('users-list'), user_to_login, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)