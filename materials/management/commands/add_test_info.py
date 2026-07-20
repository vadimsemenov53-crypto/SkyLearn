from django.core.management.base import BaseCommand
from django.core.management import call_command
from materials.models import Course, Lesson
from users.models import User, Payments

class Command(BaseCommand):

    help = 'Загрузка тестовых данных. Перед применением удаляет все данные из БД.'

    def handle(self, *args, **options):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        Payments.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Все данные удалены!'))

        try:
            call_command('loaddata', 'course.json')
            call_command('loaddata', 'lesson.json')
            call_command('loaddata', 'users.json')
            call_command('loaddata', 'payments.json')

            self.stdout.write(self.style.SUCCESS('Фикстуры загружены! Данные о покупках созданы!'))

        except Exception as e:
            self.stdout.write(self.style.WARNING(f'При загрузке данных произошла ошибка - {e}'))
