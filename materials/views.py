from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer

from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    """Контроллер для модели Course использующий ModelViewSet"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """ Метод отвечающий за перераспределение прав доступа """
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer,)

        return super().get_permissions()



class LessonCreateAPIView(CreateAPIView):
    """Контроллер создания единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """Контроллер отображения всех единиц модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Контроллер отображения единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """Контроллер редактирования единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """Контроллер удаления единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
