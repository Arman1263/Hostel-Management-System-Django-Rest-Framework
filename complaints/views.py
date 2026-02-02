from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from common.constants import UserRole
from .models import Complaint
from .serializers import ComplaintSerializer, ComplaintCreateSerializer


class ComplaintViewSet(ModelViewSet):
    queryset = Complaint.objects.select_related("student", "hostel")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return ComplaintCreateSerializer
        return ComplaintSerializer


    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.role == UserRole.ADMIN:
            return qs

        if user.role == UserRole.STUDENT:
            return qs.filter(student=user)

        if user.role == UserRole.WARDEN:
            return qs.filter(hostel=user.warden_hostel.hostel)

        return qs.none()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in [UserRole.WARDEN, UserRole.ADMIN]:
            raise PermissionError("You cannot update complaints")
        serializer.save()
