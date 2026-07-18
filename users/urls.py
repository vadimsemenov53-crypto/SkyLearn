from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = []

urlpatterns += router.urls
