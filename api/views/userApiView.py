from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import Settings, settings
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions


import jwt
from ..serializers.userSerializers import *
from ..utils import get_tokens, send_smtp
from ..models.users import CustomUser

"""
POST: Register
"""
class UserRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        newUser = CustomUser.objects.get(email=serializer.data['email'])
        newToken = get_tokens(newUser)['access']

        send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt" )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
GET: Activate Account
"""
class UserActivateView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserActivateSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({"message": "Activate Account Successfully!"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation Code Expire"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Request Password
"""
class RequestPasswordView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RequestPasswordSerializer

    def post(self, request):
        email = request.data.get('email', '')

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            newToken = get_tokens(user)['access']

            send_smtp(user, request, newToken, "Reset Password for YueYing", "reset_email.txt")

        return Response({"message": "Please check your email for futher info."}, status=status.HTTP_200_OK)


"""
GET: Validate Token for Reset Password
"""
class ResetPasswordTokenValidateView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            authToken = get_tokens(user)
            return Response(authToken, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Reset Link Expire"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


"""
PUT: Reset Password (for authenticated user only)
"""
class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data, user=self.request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.update_password()

            # When update success, should terminate the token, so it cannot be used again
        return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)

"""
POST: Login
"""
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

"""
POST: Logout
"""
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        # apparently no need to delete access token on logout, it should time out quickly enough anyway.
        # https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_204_NO_CONTENT)
