import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def test_settings(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
    settings.REST_FRAMEWORK = {
        **settings.REST_FRAMEWORK,
        "DEFAULT_THROTTLE_CLASSES": [],
    }


@pytest.fixture
def user_factory(db):
    from users.models import User

    def create_user(**kwargs):
        defaults = {
            "email":"usertest@mail.com",
            "first_name":"user",
            "last_name":"test",
        }
        password = kwargs.pop("password", "pwutest1")
        defaults.update(kwargs)

        return User.objects.create(password=password,**defaults)
    
    return create_user


@pytest.fixture
def authenticated_client(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)

    return api_client, user

