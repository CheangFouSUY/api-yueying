from django.template.loader import render_to_string
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions


import jwt
from ..serializers.userSerializers import *
from ..utils import get_tokens
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

        context = {
            'request': request,
            'protocol': request.scheme,

            # 
            'domain': settings.BACKEND_URL,
            'username': newUser.username,
            'token': str(newToken)
        }

        email = EmailMessage(
            'registration',
            render_to_string('register_email.txt', context),
            settings.EMAIL_FROM_USER, # FROM
            [newUser.email],    #TO
        )

        email.send(fail_silently=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
GET: Activate Account
"""
class UserActivateView(views.APIView):
    permissions_classes = [permissions.AllowAny]
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
POST: Login
"""
class LoginView(generics.GenericAPIView):
    permissions_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
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
