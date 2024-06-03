from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import (
    UserViewSet,
)

router = DefaultRouter()

urlpatterns = [
]
router.register("", UserViewSet, basename="users")

urlpatterns += router.urls
