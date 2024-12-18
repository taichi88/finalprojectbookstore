from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer, UserLoginSerializer

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        201: "User successfully created",
        400: "Bad request"
    }
)
@api_view(["POST"])
def register(request):
    """Handles user registration."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User successfully created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    """Handles user login."""
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: "User logged in successfully",
            400: "Invalid credentials"
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)
        return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)

class Logout(APIView):
    """Handles user logout."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: "User logged out successfully"})
    def get(self, request):
        logout(request)
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)