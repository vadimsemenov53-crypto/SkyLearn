from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (AllowAny,)

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
