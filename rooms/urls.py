from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet,
    AllocateStudentAPIView,
    VacateStudentAPIView,
)

urlpatterns = [
    path("allocate/", AllocateStudentAPIView.as_view()),
    path("vacate/<int:student_id>/", VacateStudentAPIView.as_view()),
]

router = DefaultRouter()
router.register(r"", RoomViewSet, basename="room")

urlpatterns += router.urls
