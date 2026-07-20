from rest_framework import serializers

from materials.models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons_in_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'count_lessons_in_course', 'lesson',)

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()
