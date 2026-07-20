from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer


class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentsViewSet(ModelViewSet):
    """Контроллер для модели Payments использующий ModelViewSet"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ('payment_date',)
    filterset_fields = ['course', 'lesson', 'payment_method',]