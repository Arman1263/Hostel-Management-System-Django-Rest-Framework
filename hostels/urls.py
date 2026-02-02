from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import HostelViewSet, AssignWardenAPIView

urlpatterns = [
    path("assign-warden/", AssignWardenAPIView.as_view()),
]

router = DefaultRouter()
router.register(r"", HostelViewSet, basename="hostel")

urlpatterns += router.urls
