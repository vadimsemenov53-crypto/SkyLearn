from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
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
