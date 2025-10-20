from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_register_confirmation(user_first_name, user_email):
    subject = "Welcome to the Reservation System!"
    message = f"Thank you for registering, {user_first_name}. You account has been successfully created."

    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])