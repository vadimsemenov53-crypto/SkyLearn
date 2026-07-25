from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer

from users.permissions import IsModer, IsCreator


class CourseViewSet(ModelViewSet):
    """Контроллер для модели Course использующий ModelViewSet"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """ Метод отвечающий за автоматическое заполнение владельца """
        course = serializer.save()
        course.creator = self.request.user
        course.save()

    def get_permissions(self):
        """ Метод отвечающий за перераспределение прав доступа """
        if self.action == 'create':
            self.permission_classes = (~IsModer,)

        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsCreator,)

        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsCreator,)

        return super().get_permissions()



class LessonCreateAPIView(CreateAPIView):
    """Контроллер создания единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer,)

    def perform_create(self, serializer):
        """ Метод отвечающий за автоматическое заполнение владельца """
        lesson = serializer.save()
        lesson.creator = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """Контроллер отображения всех единиц модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """Контроллер отображения единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsCreator,)


class LessonUpdateAPIView(UpdateAPIView):
    """Контроллер редактирования единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModer | IsCreator,)


class LessonDestroyAPIView(DestroyAPIView):
    """Контроллер удаления единицы модели Lesson."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer | IsCreator,)
