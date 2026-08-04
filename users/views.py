from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payments, User, Subscription
from users.permissions import IsProfile
from users.serializers import PaymentsSerializer, UserPublicSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UserPublicSerializer

        if self.action == "retrieve":
            if self.request.user != self.get_object():
                return UserPublicSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)

        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (IsProfile,)

        return super().get_permissions()


class PaymentsViewSet(ModelViewSet):
    """Контроллер для модели Payments использующий ModelViewSet"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ("payment_date",)
    filterset_fields = [
        "course",
        "lesson",
        "payment_method",
    ]


class SubscriptionAPIView(APIView):
    """ Контроллер для модели Subscription. """
    def post(self, *args, **kwargs):
        """ Переопредление метода POST. """
        user = self.request.user
        course_id = self.request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subs_obj = Subscription.objects.filter(
            user=user,
            course=course,
        )

        if subs_obj.exists():
            subs_obj.delete()
            message = "Подписка успешно удалена."

        else:
            Subscription.objects.create(
                user=user,
                course=course,
            )
            message = "Подписка успешно добавлена."


        return Response({"message": message})

