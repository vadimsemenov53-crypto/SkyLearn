from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription, User


class CourseTestCase(APITestCase):
    """Тест кейс контроллера CourseViewSet."""

    def setUp(self):
        """Начальный сет-ап с тестовыми данными."""
        self.user = User.objects.create(email="admin@gmail.com")
        self.course = Course.objects.create(name="Python", description="It's easy start", creator=self.user)
        self.course2 = Course.objects.create(name="Python", description="It's easy start")
        self.lesson = Lesson.objects.create(
            name="Start_1",
            description="First_lesson",
            video_url="https://www.youtube.com/watch?v=777777c",
            course=self.course,
            creator=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_list(self):
        """Тестирование получаемых данных для -> materials:course-list."""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "amount": None,
                    "count_lessons_in_course": 1,
                    "lesson": [
                        {
                            "id": self.lesson.pk,
                            "video_url": self.lesson.video_url,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "image": None,
                            "course": self.course.pk,
                            "creator": self.user.pk,
                        },
                    ],
                    "creator": self.user.pk,
                    "is_subscribed": False,
                },
                {
                    "id": self.course2.pk,
                    "name": self.course2.name,
                    "description": self.course2.description,
                    "amount": None,
                    "count_lessons_in_course": 0,
                    "lesson": [],
                    "creator": None,
                    "is_subscribed": False,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Course.objects.all().count(), 2)

        self.assertTrue(Course.objects.all().exists())

        self.assertEqual(data, result)

    def test_course_retrieve(self):
        """Тестирование получаемых данных для -> materials:course-detail."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        """Тестирование создания курса для -> materials:course-list."""
        url = reverse("materials:course-list")
        data = {"name": "JAVA", "description": "Develop for start students"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.all().count(), 3)

        self.assertEqual(response.data["name"], data["name"])

    def test_course_create_is_moder(self):
        """Тестирование создания курса (модератор) для -> materials:course-list."""
        moder_group = Group.objects.create(name="moderator")
        self.user.groups.add(moder_group)

        url = reverse("materials:course-list")
        data = {"name": "JAVA", "description": "Develop for start students"}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.json(), {"detail": "У вас недостаточно прав для выполнения данного действия."})

    def test_course_update(self):
        """Тестирование обновление данных курса для -> materials:course-detail."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Python 2026",
        }

        response = self.client.patch(url, data, format="json")
        data_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data_json.get("name"), data["name"])

    def test_course_delete(self):
        """Тестирование удаление данных курса для -> materials:course-detail."""
        url = reverse("materials:course-detail", args=(self.course.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 1)

    def test_course_delete_is_moder(self):
        """Тестирование удаление данных курса (модератор) для -> materials:course-detail."""
        moder_group = Group.objects.create(name="moderator")
        self.user.groups.add(moder_group)

        url = reverse("materials:course-detail", args=(self.course2.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.json(), {"detail": "У вас недостаточно прав для выполнения данного действия."})

    def test_course_subscription(self):
        """Тестирование подписки на курс для -> materials:subscription."""
        url = reverse("materials:subscription")
        data = {
            "course_id": self.course.pk,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


class LessonTestCase(APITestCase):
    """Тест кейс контроллеров модели Lesson."""

    def setUp(self):
        """Начальный сет-ап с тестовыми данными."""
        self.user = User.objects.create(email="admin@gmail.com")
        self.lesson = Lesson.objects.create(
            name="Start_1",
            description="First_lesson",
            video_url="https://www.youtube.com/watch?v=777777c",
            creator=self.user,
        )
        self.lesson2 = Lesson.objects.create(
            name="Start_2",
            description="First_lesson2",
            video_url="https://www.youtube.com/watch?v=7777772c",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        """Тестирование получаемых данных для -> materials:lessons_list."""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "image": None,
                    "course": None,
                    "creator": self.user.pk,
                },
                {
                    "id": self.lesson2.pk,
                    "video_url": self.lesson2.video_url,
                    "name": self.lesson2.name,
                    "description": self.lesson2.description,
                    "image": None,
                    "course": None,
                    "creator": None,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Lesson.objects.all().count(), 2)

        self.assertTrue(Lesson.objects.all().exists())

        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        """Тестирование получаемых данных для -> materials:lessons_retrieve."""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создания урока для -> materials:lessons_create."""
        url = reverse("materials:lessons_create")
        data = {
            "name": "JAVA",
            "description": "Develop for start students",
            "video_url": "https://www.youtube.com/watch?v=777777c",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 3)

        self.assertEqual(response.data["name"], data["name"])

    def test_lesson_create_is_moder(self):
        """Тестирование создания урока (модератор) для -> materials:lessons_create."""
        moder_group = Group.objects.create(name="moderator")
        self.user.groups.add(moder_group)

        url = reverse("materials:lessons_create")
        data = {
            "name": "JAVA",
            "description": "Develop for start students",
            "video_url": "https://www.youtube.com/watch?v=777777c",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.json(), {"detail": "У вас недостаточно прав для выполнения данного действия."})

    def test_lesson_update(self):
        """Тестирование обновление данных урока для -> materials:lessons_update."""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Start_2027",
        }

        response = self.client.patch(url, data, format="json")
        data_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data_json.get("name"), data["name"])

    def test_lesson_delete(self):
        """Тестирование удаление данных урока для -> materials:lessons_delete."""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_delete_is_moder(self):
        """Тестирование удаление данных урока (модератор) для -> materials:lessons_delete."""
        moder_group = Group.objects.create(name="moderator")
        self.user.groups.add(moder_group)

        url = reverse("materials:lessons_delete", args=(self.lesson2.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(response.json(), {"detail": "У вас недостаточно прав для выполнения данного действия."})
