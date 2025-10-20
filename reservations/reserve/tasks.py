from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_reservation_confirmation(reservation_id, user_email):
    subject = "Reservation Confirmation"
    message = f"Your reservation with the ID {reservation_id} has been successfully created."

    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])