# Create your tests here.

# accommodation/tests.py
 
# some random test, TODO.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Owner, Accommodation

class AccommodationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = Owner.objects.create(name='Test Owner', contact='test@example.com')
        self.accommodation = Accommodation.objects.create(
            title='Test Apartment',
            description='A test apartment',
            type='apartment',
            price=8000,
            beds=2,
            bedrooms=1,
            latitude=22.2830,
            longitude=114.1370,
            geo_address='Test Address',
            available_from='2023-01-01',
            available_until='2023-12-31',
            owner=self.owner
        )
        
    def test_get_all_accommodations(self):
        response = self.client.get(reverse('accommodation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_accommodation(self):
        data = {
            'title': 'New Apartment',
            'description': 'A new test apartment',
            'type': 'apartment',
            'price': 10000,
            'beds': 3,
            'bedrooms': 2,
            'latitude': 22.2800,
            'longitude': 114.1300,
            'geo_address': 'New Address',
            'available_from': '2023-02-01',
            'available_until': '2023-11-30',
            'owner_id': self.owner.id
        }
        response = self.client.post(reverse('accommodation-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_filter_by_type(self):
        response = self.client.get(f"{reverse('accommodation-list')}?type=apartment")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        response = self.client.get(f"{reverse('accommodation-list')}?type=house")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_distance_filter(self):
        # Main campus is at (22.283, 114.137)
        response = self.client.get(f"{reverse('accommodation-list')}?near_campus=main&max_distance=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should find our test accommodation
        
        response = self.client.get(f"{reverse('accommodation-list')}?near_campus=main&max_distance=0.1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should be too close to find anything