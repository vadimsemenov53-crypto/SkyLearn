from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

def send_information_email(subject: str, message: str, email_list: list[str]):
    """ Функция отправки сообщений на почту.
     (принимает subject - тема письма, message - тело сообщения, email_list - список emails для рассылки) """
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=email_list
    )