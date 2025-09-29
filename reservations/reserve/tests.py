from django.test import TestCase
from django.urls import reverse
from .models import Reservation, Location
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class LocationTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.user = User.objects.create_user(username='user', password='userpass')
        self.location = Location.objects.create(name='Meeting room', address_line='45th street', capacity=10)
        self.list_url = reverse('location-list')
        self.url = reverse('location-detail', args=[self.location.pk])

    def test_get_location_authorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.location.name)

    def test_list_locations(self):
        #self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location_unauthorized(self):
        data = {"name": "2nd Meeting Room"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_location_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_location_only_admin(self):
        self.client.login(username='user', password='userpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Location.objects.filter(pk=self.location.pk).exists())

        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Location.objects.filter(pk=self.location.pk).exists())



