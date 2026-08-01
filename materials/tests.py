from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    """ Тест кейс контроллера CourseViewSet. """

    def setUp(self):
        """ Начальный сет-ап с тестовыми данными. """
        self.user = User.objects.create(email="admin@gmail.com")
        self.course = Course.objects.create(name="Python", description="It's easy start", creator=self.user)
        self.lesson = Lesson.objects.create(
            name="Start_1",
            description="First_lesson",
            video_url="https://www.youtube.com/watch?v=777777c",
            course=self.course,
            creator=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_list(self):
        """ Тестирование получаемых данных для -> materials:course-list. """
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "count_lessons_in_course": 1,
                    "lesson": [
                        {
                            "id": self.lesson.pk,
                            "video_url": self.lesson.video_url,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "image": None,
                            "course": self.course.pk,
                            "creator": self.user.pk
                        },
                    ],
                    "creator": self.user.pk,
                    "is_subscribed": False
                }
            ]}

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Course.objects.all().count(), 1
        )

        self.assertTrue(
            Course.objects.all().exists()
        )

        self.assertEqual(data, result)


    def test_course_retrieve(self):
        """ Тестирование получаемых данных для -> materials:course-detail. """
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data.get('name'),
            self.course.name
        )

    def test_course_create(self):
        """ Тестирование создания курса для -> materials:course-list. """
        url = reverse("materials:course-list")
        data = {
            "name": "JAVA",
            "description": "Develop for start students"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Course.objects.all().count(), 2
        )

        self.assertEqual(
            response.data['name'], data["name"]
        )

    def test_course_update(self):
        """ Тестирование обновление данных курса для -> materials:course-detail. """
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Python 2026",
        }

        response = self.client.patch(url, data, format='json')
        data_json = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data_json.get('name'),
            data['name']
        )

    def test_course_delete(self):
        """ Тестирование удаление данных курса для -> materials:course-detail. """
        url = reverse("materials:course-detail", args=(self.course.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Course.objects.all().count(), 0
        )


class LessonTestCase(APITestCase):
    """ Тест кейс контроллера CourseViewSet. """