import pytest
from users.models import User

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@mail.com",
        password="passwordadmin",
        first_name="admin",
        last_name="admin",
    )

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email="user@mail.com",
        password="passworduser",
        first_name="user",
        last_name="user",
    )