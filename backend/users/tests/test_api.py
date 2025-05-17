from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserAuthTests(APITestCase):

    def test_user_signup_success(self):
        response = self.client.post(reverse('signup'), {
            "username": "newuser",
            "password": "newpassword123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_signup_duplicate_username(self):
        User.objects.create_user(username="existinguser", password="pass")
        response = self.client.post(reverse('signup'), {
            "username": "existinguser",
            "password": "pass"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        User.objects.create_user(username="loginuser", password="test1234")
        response = self.client.post(reverse('token_obtain_pair'), {
            "username": "loginuser",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_failure(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            "username": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)