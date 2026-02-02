from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsAdmin

from rest_framework import status
from common.constants import UserRole
from .serializers import UserCreateSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email,
            "role": request.user.role
        })

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Hello Admin"})


class CreateStudentAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role=UserRole.STUDENT)
            return Response(
                {
                    "message": "Student created successfully",
                    "email": user.email,
                    "role": user.role
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateWardenAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role=UserRole.WARDEN)
            return Response(
                {
                    "message": "Warden created successfully",
                    "email": user.email,
                    "role": user.role
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


