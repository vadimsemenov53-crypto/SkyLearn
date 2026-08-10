import stripe
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payments, User, Subscription
from users.permissions import IsProfile, IsModer
from users.serializers import PaymentsSerializer, UserPublicSerializer, UserSerializer, SubscriptionSerializer, \
    SubscriptionAllSerializer

from users.services import create_stripe_payment, check_stripe_payment

class UserViewSet(ModelViewSet):
    """Контроллер для модели User использующий ModelViewSet"""
    queryset = User.objects.all()

    @swagger_auto_schema(responses={200: UserPublicSerializer})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
        "payment_method",
    ]

    def perform_create(self, serializer):
        """ Переопределение метода создания: Пользователь -> фактический кто создал запрос, сумма берется из модели курса. """
        course = serializer.validated_data["course"]

        try:
            session_id, link = create_stripe_payment(course=course)

        except stripe.StripeError as error:
            raise ValidationError(f"Ошибка Stripe: {str(error)}")

        serializer.save(
            user=self.request.user,
            amount=course.amount,
            session_id=session_id,
            link=link,
            status=course.P_PENDING,
        )


class PaymentStatusAPIView(APIView):
    """ Контроллер проверки статуса платежа Stripe. """

    def get(self, request, pk):
        """ Метод получения данных о статусе платежа. """
        payment = get_object_or_404(Payments, id=pk, user=request.user)

        status_stripe = check_stripe_payment(payment.session_id)

        if status_stripe == "paid":
            payment.payment_method = Payments.P_PAID
            payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "status": payment.payment_method,
            }
        )



class SubscriptionViewSet(ModelViewSet):
    """Контроллер для модели Course использующий ModelViewSet"""
    serializer_class = SubscriptionAllSerializer
    permission_classes = (~IsModer,)

    def get_queryset(self):
        """ Метод возвращает подписки пользователя. """
        return Subscription.objects.filter(
            user=self.request.user
        )

    @action(detail=True, methods=("post",))
    def seen_update(self, request, pk):
        """ Метод отмечает обновление курса как просмотренное (проставляет дату просмотра). """
        subs = get_object_or_404(Subscription, pk=pk, user=request.user)
        subs.last_seen_update_at = timezone.now()
        subs.save(update_fields=["last_seen_update_at"])

        return Response({
            "message": "Обновление отмечено как просмотренное."
        })

class SubscriptionAPIView(APIView):
    """ Контроллер для модели Subscription. """
    @swagger_auto_schema(
        operation_summary="Подписка на курс",
        operation_description="""
            Если пользователь уже подписан на курс — подписка удаляется.
            Если пользователь не подписан — создается новая подписка.
            """,
        request_body=SubscriptionSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Результат операции (добавлена / удалена)"
            ),
            status.HTTP_404_NOT_FOUND: "Курс не найден",
        },
    )
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

