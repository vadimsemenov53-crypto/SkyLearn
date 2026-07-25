from django.db import models
from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Модель для представления Курса."""

    name = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название курса")
    image = models.ImageField(
        upload_to="course/image",
        verbose_name="Превью",
        help_text="Загрузите превью(картинку)",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )

    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель для представления урока."""

    name = models.CharField(max_length=100, verbose_name="Название", help_text="Введите название урока")
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="course/image",
        verbose_name="Превью",
        help_text="Загрузите превью(картинку)",
        blank=True,
        null=True,
    )
    video_url = models.URLField(max_length=500, verbose_name="Ссылка на видео", help_text="Передайте ссылку на видео")

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выбери курс урока",
        related_name="lesson",
    )

    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
