from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from materials.models import Course
from materials.services import send_information_email
from users.models import Subscription


@shared_task
def send_information_about_update(course_id):
    """Отложенная задача для отправки уведомлений об изменении материалов курса (урока)."""

    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(
        course=course,
        is_active=True,
    )

    email_list = [subscription.user.email for subscription in subscriptions if subscription.user.email]

    if not email_list:
        return

    send_information_email(
        subject=f"Обновление курса: {course.name}",
        message="Вам доступны новые материалы курса, ознакомьтесь с новыми данными.",
        email_list=email_list,
    )


@shared_task
def send_information_about_update_periodical():
    """Периодическая задача (1 раз в час) просматривает все подписки клиентов и крайние обновления курса.
    Если пользователь не ознакомился с последним обновлением в течение 4 часов - отправляет на почту сообщение."""
    email_list = []
    now = timezone.now()

    subscriptions = Subscription.objects.filter(
        is_active=True,
    ).select_related(
        "course",
        "user",
    )

    for subscription in subscriptions:
        course = subscription.course

        if subscription.last_seen_update_at is None or subscription.last_seen_update_at < course.updated_at:

            if now - course.updated_at >= timedelta(hours=4):
                email_list.append(subscription.user.email)

    if email_list:
        send_information_email(
            subject="SKYLEARN - обновление",
            message="Напоминаем, проверьте обновления материалов ваших подписок.",
            email_list=email_list,
        )
