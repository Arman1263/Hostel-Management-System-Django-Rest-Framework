from django.urls import path
from .views import ProfileView
from .views import AdminOnlyView
from .views import CreateStudentAPIView, CreateWardenAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
]

urlpatterns += [
    path("me/", ProfileView.as_view()),
]

urlpatterns += [
    path("admin-test/", AdminOnlyView.as_view()),
]

urlpatterns += [
    path("create-student/", CreateStudentAPIView.as_view()),
    path("create-warden/", CreateWardenAPIView.as_view()),
]


