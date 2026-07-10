from unittest.mock import patch
from users.services import UserNotificationService


@patch("users.services.send_register_confirmation.delay")
def test_confirmation_account_with_correct_data(mock_delay, user_factory):
    user = user_factory(first_name="User", email="utestuser@mail.com")
    UserNotificationService.send_account_confirmation(user)
    mock_delay.assert_called_once_with("User", "utestuser@mail.com")