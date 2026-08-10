from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def check_last_login_user():
    """ Периодическая задача для проверки последнего входа пользователя.
     Если пользователь не заходил месяц и более его аккаунт блокируется
     -> is_active = False."""
    month_ago = timezone.now() - timedelta(days=30)
    days_for_login = timezone.now() - timedelta(days=10)
    users = User.objects.filter(is_active=True)

    for user in users:
        if user.last_login and user.last_login < month_ago:
            user.is_active = False
            user.save(update_fields=["is_active"])

        elif user.last_login is None and user.date_joined < days_for_login:
            user.is_active = False
            user.save(update_fields=["is_active"])
