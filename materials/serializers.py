from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import YouTubeValidateVideoURL
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeValidateVideoURL()], help_text="Ссылка на видео YouTube")

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "amount",
            "count_lessons_in_course",
            "lesson",
            "creator",
            "is_subscribed",
            "updated_at",
        )

    def get_count_lessons_in_course(self, course):
        """ Метод подсчета уроков на данном курсе. """
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, obj):
        """ Метод получения активности подписки пользователя на данный курс. """
        user = self.context['request'].user

        return Subscription.objects.filter(user=user, course=obj).exists()