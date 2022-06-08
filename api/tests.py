from django.test import TestCase
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework import status
from django.urls import reverse
from django.core import mail
from django.conf import settings
import jwt


class TestRegister(APITestCase):
    """
    A class for testing registration. Checks correct email is sent out without actually sending emails.
    Checks email token correctly encodes user ID.
    """

    def setUp(self):
        self.url=reverse("register")

    def test_register_email_is_sent(self):
        data = {"email" : "test@email.com", "username": "cattest", "password": "Mango11.", "password2": "Mango11.", "securityQuestion": 1, "securityAnswer": "blue"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual("Activate Account", mail.outbox[0].subject)
        self.assertEqual("seyueying2022@gmail.com", mail.outbox[0].from_email)
        self.assertEqual("test@email.com", mail.outbox[0].to[0])

    def test_register_token(self):
        # integration testing was done in postman with real email sending / actually following email link.
        data = {"email" : "test@email.com", "username": "cattest", "password": "Mango11.", "password2": "Mango11.", "securityQuestion": 1, "securityAnswer": "blue"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # partition by looking at the format of the register.txt in templates dir
        token = mail.outbox[0].body.partition("?token=")[2].partition("\n\n\n\n您好")[0].strip()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        user = CustomUser.objects.get(id=payload['user_id'])
        self.assertEqual(user.username, "cattest")

class TestLogin(APITestCase):
    """
    A class for testing successfull and unsuccessfull logon attempts..
    """

    def setUp(self):
        self.url=reverse("login")
        self.active_cat = CustomUser.objects.create_user(email="cat@gmail.com", username="cat", password="Mango11.", is_active=True)
        self.inactive_dog = CustomUser.objects.create_user(email="dog@gmail.com", username="dog", password="Apple11.", is_active=False)

    def test_good_logon(self):
        data = {"username": "cat", "password": "Mango11."}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_view_accessible_with_token(self):
        data = {"username": "cat", "password": "Mango11."}
        response_login = self.client.post(self.url, data, format='multipart')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + TokensFromResponse(response_login).access)
        data = {"refresh": TokensFromResponse(response_login).refresh}
        response_logout = self.client.post(reverse("logout"), data)
        self.assertEqual(response_logout.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_view_inaccessible_without_token(self):
        data = {"refresh": "yosh hahaha"}
        response_logout = self.client.post(reverse("logout"), data)
        self.assertEqual(response_logout.status_code, status.HTTP_403_FORBIDDEN)

    def test_bad_username(self):
        data = {"username": "catbo", "password": "Mango11."}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_username(self):
        data = {"username": "", "password": "Mango11."}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password(self):
        data = {"username": "cat", "password": "#MangoesAreEvil"}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_password(self):
        data = {"username": "cat", "password": ""}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        data = {"username": "dog", "password": "Apple11."}
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual("no access token", TokensFromResponse(response).access)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TokensFromResponse():

    def __init__(self, response):
        self.access="no access token"
        self.refresh="no refresh token"
        try:
            self.access = response.json()['tokens']['access']
            self.refresh = response.json()['tokens']['refresh']
        except KeyError:
            pass
