from celery import shared_task
from materials.services import send_information_email
from users.models import Subscription
from materials.models import Course


@shared_task
def send_information_about_update(course_id):
    """ Отложенная задача для отправки уведомлений об изменении материалов курса (урока). """

    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True,)

    email_list = [
        subscription.user.email
        for subscription in subscriptions
        if subscription.user.email
    ]

    if not email_list:
        return

    send_information_email(
        subject=f"Обновление курса: {course.name}",
        message="Вам доступны новые материалы курса, ознакомьтесь с новыми данными.",
        email_list=email_list
    )
