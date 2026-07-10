from .tasks import send_register_confirmation

class UserNotificationService:
    @staticmethod
    def send_account_confirmation(user):
        send_register_confirmation.delay(user.first_name, user.email)

    #TODO: Password recovery mail