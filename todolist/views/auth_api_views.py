from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class RegisterAPIView(APIView):
    """
    Register user + return token
    """
    permission_classes = [AllowAny]   # ✅ IMPORTANT
    authentication_classes = [] 
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([username, email, password]):
            return Response(
                {"detail": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)  # IMPORTANT for template auth

        return Response(
            {
                "message": "Registration successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            },
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    """
    Login user + return token
    """
    permission_classes = [AllowAny]   # ✅ IMPORTANT
    authentication_classes = []
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )
        print(request.data.get("username"),request.data.get("password"))
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        print("Authenticated user:",user)
        login(request, user)  

        return Response(
            {
                "message": "Login successful",
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                }
            }
        )


class LogoutAPIView(APIView):
    """
    Logout user
    """

    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)

        return Response({"message": "Logged out"})
