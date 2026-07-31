from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import YouTubeValidateVideoURL


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeValidateVideoURL()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "count_lessons_in_course",
            "lesson",
            "creator",
        )

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()
