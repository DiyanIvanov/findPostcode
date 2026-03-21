from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Postcode


class PostcodeViewTest(APITestCase):

    def setUp(self):
        self.valid_url = reverse('get_postcode', kwargs={'postcode': 'b1+1ay'})
        self.invalid_url = reverse('get_postcode', kwargs={'postcode': 'b1-1ay'})
        self.missing_postcode_url = '/api/postcode/'
        self.postcode = Postcode.objects.create(
            postcode = "B1 1AY",
            district = "B1",
            area = "B",
            eastings = "406523",
            northings = "286448",
            latitude = "-1.9156917",
            longitude = "52.4759231"
        )

    def test_missing_postcode_test_returns_400(self):
        response = self.client.get(self.missing_postcode_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_postcode_returns_200(self):
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_postcode_returns_404(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

