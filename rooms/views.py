from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from common.permissions import IsAdminOrWarden
from .models import Room
from .serializers import RoomSerializer

from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from .models import RoomAllocation
from .serializers import RoomAllocationSerializer


# Create your views here.
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.select_related("hostel")
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrWarden]

    def get_queryset(self):
        queryset = super().get_queryset()
        hostel_id = self.request.query_params.get("hostel")
        if hostel_id:
            queryset = queryset.filter(hostel_id=hostel_id)
        return queryset


class AllocateStudentAPIView(APIView):
    permission_classes = [IsAdminOrWarden]

    @transaction.atomic
    def post(self, request):
        serializer = RoomAllocationSerializer(data=request.data)
        if serializer.is_valid():
            allocation = serializer.save()
            return Response(
                {
                    "message": "Student allocated successfully",
                    "student": allocation.student.email,
                    "room": allocation.room.room_number,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VacateStudentAPIView(APIView):
    permission_classes = [IsAdminOrWarden]

    def post(self, request, student_id):
        try:
            allocation = RoomAllocation.objects.get(student_id=student_id)
            allocation.delete()
            return Response(
                {"message": "Student vacated successfully"},
                status=status.HTTP_200_OK
            )
        except RoomAllocation.DoesNotExist:
            return Response(
                {"detail": "Student is not allocated to any room"},
                status=status.HTTP_400_BAD_REQUEST
            )


def get_warden_hostel(user):
    return user.warden_hostel.hostel


def get_queryset(self):
    qs = super().get_queryset()

    if self.request.user.role == "WARDEN":
        qs = qs.filter(hostel=get_warden_hostel(self.request.user))

    return qs
