from unittest.mock import patch
import pytest

@pytest.mark.django_db
def test_register_create_user_mail_trigger(api_client):
    with patch("users.services.send_register_confirmation.delay") as mock_delay:
        response = api_client.post("/api/register/", {
            "email": "new@mail.com",
            "password": "securepw121",
            "password2": "securepw121",
            "first_name": "new",
            "last_name": "user",
        })

    assert response.status_code == 201
    mock_delay.assert_called_once_with("new", "new@mail.com")


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    response = api_client.post("/api/login/", {
        "email": "invalidmail@mail.com",
        "password": "invalidpw",
    })

    assert response.status_code == 401