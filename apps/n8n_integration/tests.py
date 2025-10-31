from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import YourModel  # Replace with your actual model

class N8NIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/your-endpoint/'  # Replace with your actual endpoint

    def test_create_data(self):
        data = {
            'field1': 'value1',  # Replace with your actual fields and values
            'field2': 'value2',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(YourModel.objects.count(), 1)  # Replace with your actual model
        self.assertEqual(YourModel.objects.get().field1, 'value1')  # Replace with your actual fields

    def test_get_data(self):
        # Create a sample object to test retrieval
        YourModel.objects.create(field1='value1', field2='value2')  # Replace with your actual fields
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Adjust based on your expected response

    def test_invalid_data(self):
        data = {
            'field1': '',  # Invalid data
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)