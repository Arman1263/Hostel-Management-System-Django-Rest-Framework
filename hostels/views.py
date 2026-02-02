from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from common.permissions import IsAdmin
from .models import Hostel
from .serializers import HostelSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.permissions import IsAdmin
from .models import WardenHostel
from .serializers import WardenHostelAssignSerializer


# Create your views here.
class HostelViewSet(ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class AssignWardenAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = WardenHostelAssignSerializer(data=request.data)
        if serializer.is_valid():
            assignment = serializer.save()
            return Response(
                {
                    "message": "Warden assigned successfully",
                    "warden": assignment.warden.email,
                    "hostel": assignment.hostel.name,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
