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
    """ Модель для представления платежей. """
    P_CASH = "cash"
    P_REMITTANCE = "remittance"

    PAYMENTS_METHOD_CHOICES = [
        (P_CASH, "Наличные"),
        (P_REMITTANCE, "Перевод"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя совершившего покупку',
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Купленный курс',
        help_text='Укажите купленный курс',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Купленный урок',
        help_text='Укажите купленный урок',
    )
    amount = models.PositiveIntegerField(verbose_name='Сумма покупки', help_text='Укажите сумму покупки')
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENTS_METHOD_CHOICES,
        default=P_REMITTANCE,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f'{self.user} - {self.amount}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-payment_date",)

