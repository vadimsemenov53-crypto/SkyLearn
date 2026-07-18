from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
