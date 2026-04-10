from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class RegisterUserTestCase(APITestCase):
    def setUp(self):
        self.username = "john"
        self.email = "john.dow@findpostcode.com"
        self.password = "MySuperPass@123"
        self.first_name = "John"
        self.last_name = "Doe"

        self.url = reverse('register')

    def test_register_user_valid_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_email(self):
        data = {
            "username": self.username,
            "password": self.password,
            "email": "",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        data = {
            "username": self.username,
            "email": "invalid@email",
            "password": self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password": 123,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_missing_username(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password(self):
        data = {
            "email": self.email,
            "username": self.username,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)