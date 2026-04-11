from rest_framework.test import APITestCase
from api.throttles import DailyThrottleRate, PerMinuteThrottleRate
from django.urls import reverse
from api.models import Postcode
from accounts.models import FindPostcodeUser
from rest_framework.authtoken.models import Token
from django.core.cache import cache
from unittest.mock import patch


class UserRateThrottleTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = FindPostcodeUser.objects.create_user(
            username='test_user',
            password='testp@ssword123',
            email='test_email@findpostcode.com',
        )
        user = FindPostcodeUser.objects.get(username='test_user')
        self.token, _ = Token.objects.get_or_create(user=user)
        self.url = reverse('get_postcode', kwargs={'postcode': 'b1+1ay'})
        self.postcode = Postcode.objects.create(
            postcode="B1 1AY",
            district="B1",
            area="B",
            eastings=406523,
            northings=286448,
            latitude=52.4759231,
            longitude=-1.9156917
        )

    def test_daily_rate(self):
        cache.clear()
        with patch.object(DailyThrottleRate, 'get_rate', return_value='3/day'):
            for i in range(3):
                response = self.client.get(
                    self.url,
                    HTTP_AUTHORIZATION=f'Token {self.token.key}'
                )
                self.assertEqual(response.status_code, 200)

            response = self.client.get(
                self.url,
                HTTP_AUTHORIZATION=f'Token {self.token.key}'
            )
            self.assertEqual(response.status_code, 429)

    def test_daily_per_minute_rate(self):
        cache.clear()
        with patch.object(PerMinuteThrottleRate, 'get_rate', return_value='3/min'):
            for i in range(3):
                response = self.client.get(
                    self.url,
                    HTTP_AUTHORIZATION=f'Token {self.token.key}'
                )
                self.assertEqual(response.status_code, 200)

            response = self.client.get(
                self.url,
                HTTP_AUTHORIZATION=f'Token {self.token.key}'
            )
            self.assertEqual(response.status_code, 429)

