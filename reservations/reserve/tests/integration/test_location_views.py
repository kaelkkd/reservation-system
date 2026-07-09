import pytest
from django.urls import reverse
from reserve.models import Location
from rest_framework import status


pytestmark = pytest.mark.django_db

@pytest.fixture
def location(db):
    return Location.objects.create(name="Meeting room", address_line="45th street", 
                                   country="BR", capacity=10, is_available=True)

@pytest.fixture
def list_url():
    return reverse("location-list")

@pytest.fixture
def detail_url(location):
    return reverse("location-detail", args=[location.pk])

def test_get_location_returns_200(api_client, detail_url, location):
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == location.name

def test_get_locations_list_returns_200(api_client, list_url):
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK

def test_update_location_unauthenticated_returns_401(api_client, detail_url):
    response = api_client.put(detail_url, {"name": "Old Bedroom 21"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_location_unauthenticated_returns_401(api_client, detail_url):
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
def test_delete_location_unauthorized_returns_403(api_client, regular_user, detail_url, location):
    api_client.force_authenticate(user=regular_user)
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Location.objects.filter(pk=location.pk).exists()

def test_delete_location_admin_returns_204(api_client, admin_user, detail_url, location):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Location.objects.filter(pk=location.pk).exists()

