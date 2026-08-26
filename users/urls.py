from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentStatusAPIView, PaymentsViewSet, SubscriptionViewSet, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentsViewSet, basename="payments")
router.register(r"subs", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "payments/<int:pk>/",
        PaymentStatusAPIView.as_view(),
        name="payments_status",
    ),
]

urlpatterns += router.urls
