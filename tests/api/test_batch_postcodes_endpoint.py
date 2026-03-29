from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Postcode
from accounts.models import FindPostcodeUser
from rest_framework.authtoken.models import Token


class BatchPostcodeAPITestCase(APITestCase):
    def setUp(self):
        self.user = FindPostcodeUser.objects.create_user(
            username='test_user',
            password='testp@ssword123',
        )
        self.postcode_one = Postcode.objects.create(
            postcode = 'B1 1AY',
            district = 'B1',
            area = 'B',
            eastings = 406523,
            northings = 286448,
            latitude = 52.4759231,
            longitude = -1.9156917
        )
        self.postcode_two = Postcode.objects.create(
            postcode='M1 1AE',
            district='M1',
            area='M',
            eastings=384756,
            northings=398553,
            latitude=53.483487,
            longitude=-2.231182
        )
        self.url = reverse('batch_endpoint')

        user = FindPostcodeUser.objects.get(username='test_user')
        self.token, _ = Token.objects.get_or_create(user=user)

    def test_batch_endpoint_with_both_valid_and_invalid_postcodes(self):
        data = {
            "postcodes": ["B1 1AY", "Invalid"]
        }


        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_output = [
            {
                'postcode': 'B1 1AY',
                'district': 'B1',
                'area': 'B',
                'eastings': 406523,
                'northings': 286448,
                'latitude': 52.4759231,
                'longitude': -1.9156917
            },
            {
                'postcode': 'INVALID',
                'error': 'Not found'
            }
        ]

        self.assertEqual(response.json(), expected_output)

    def test_not_authenticated_request_returns_405(self):
        data = {
            "postcodes": ["B1 1AY", "Invalid"]
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_get_requests_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_requests_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_requests_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_requests_not_allowed(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
