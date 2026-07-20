from rest_framework.viewsets import ModelViewSet

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer