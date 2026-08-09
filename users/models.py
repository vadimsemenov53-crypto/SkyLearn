from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите адрес эл.почты")
    phone = PhoneNumberField(
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона.",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Введите ваш город",
        blank=True,
        null=True,
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Модель для представления платежей."""

    P_PENDING = "pending"
    P_PAID = "paid"

    PAYMENTS_STATUS_CHOICES = [
        (P_PENDING, "Ожидает оплаты"),
        (P_PAID, "Оплачено"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя совершившего покупку",
        related_name="payments",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Купленный курс",
        help_text="Укажите купленный курс",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма покупки", help_text="Укажите сумму покупки")
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENTS_STATUS_CHOICES,
        default=P_PENDING,
        verbose_name="Статус оплаты",
    )

    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        help_text="Укажите Id сессии",
        blank=True,
        null=True,
    )

    link = models.URLField(
        max_length=1000,
        verbose_name="Ссылка оплаты",
        help_text="Укажите ссылку для оплаты",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user} - {self.amount}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-payment_date",)



class Subscription(models.Model):
    """ Модель для представления Подписки. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выбери курс урока",
        related_name="subscriptions",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность"
    )

    last_seen_update_at = models.DateTimeField(
        verbose_name="Последнее обновление материала",
        help_text="Укажите дату последнего обновления материала",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")
