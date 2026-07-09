import uuid
from unittest.mock import patch, MagicMock
from reserve.services import ReservationService

@patch("reserve.services.send_reservation_confirmation")
def test_confirm_creation_dispatches_task_with_correct_args(mock_task):
    reservation = MagicMock()
    reservation.reservation_id = uuid.uuid4()
    reservation.reserved_by.email = "user@test.com"
    ReservationService.confirm_reservation(reservation)

    mock_task.delay.assert_called_once_with(str(reservation.reservation_id), "user@test.com")

@patch("reserve.services.send_cancellation_confirmation")
def test_confirm_cancellation_dispatches_task_with_correct_args(mock_task):
    reservation = MagicMock()
    reservation.reservation_id = uuid.uuid4()
    reservation.reserved_by.email = "user@test.com"
    ReservationService.confirm_cancellation(reservation)

    mock_task.delay.assert_called_once_with(str(reservation.reservation_id), "user@test.com")