from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions


import jwt
from ..serializers.userSerializers import *
from ..utils import get_tokens, send_smtp
from ..models.users import CustomUser
from ..models.userRelations import *

"""
POST: Register
"""
class UserRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        try: 
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            newUser = CustomUser.objects.get(email=serializer.data['email'])
            newToken = get_tokens(newUser)['access']

            send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt" )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Register Failed"}, status=status.HTTP_400_BAD_REQUEST)

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
                user.updatedAt = timezone.now()
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
        try: 
            email = request.data.get('email', '')
            username = request.data.get('username', '')

            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                if not user.username == username: # incase the username is not the same as email
                    return Response({"message": "Invalid Username or Email"}, status=status.HTTP_400_BAD_REQUEST)
                newToken = get_tokens(user)['access']
                send_smtp(user, request, newToken, "Reset Password for YueYing", "reset_email.txt")
                return Response({"message": "Please check your email for futher info."}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Failed to Request Password"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"message": "Reset Link Expire"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


"""
PUT: Reset Password (for authenticated user only)
"""
class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        try:
            serializer = self.get_serializer(data=request.data, user=self.request.user)
            if serializer.is_valid(raise_exception=True):
                serializer.updatePassword()
                # When update success, should terminate the token, so it cannot be used again
                return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Password Reset Failed"}, status=status.HTTP_400_BAD_REQUEST)


# class RequestPasswordBySecurityQuestionView(generics.GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = RequestPasswordSerializer
#     def post(self, request):
#         try: 
#             email = request.data.get('email', '')
#             username = request.data.get('username', '')

#             if CustomUser.objects.filter(email=email).exists():
#                 user = CustomUser.objects.get(email=email)
#                 if not user.username == username: # incase the username is not the same as email
#                     return Response({"message": "Invalid Username or Email"}, status=status.HTTP_400_BAD_REQUEST)
                
#                 newToken = get_tokens(user)['access']
#                 send_smtp(user, request, newToken, "Reset Password for YueYing", "reset_email.txt")
#                 return Response({"message": "Please check your email for futher info."}, status=status.HTTP_200_OK)
#         except:
#             return Response({"message": "Failed to Request Password"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Login
"""
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status= status.HTTP_200_OK)

"""
POST: Logout
"""
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            # apparently no need to delete access token on logout, it should time out quickly enough anyway.
            # https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message": "Logout Failed"}, status=status.HTTP_400_BAD_REQUEST)


""" For Admin(superuser)
GET: Get User Detail By Id  # for any
PUT: Update User By Id      # for superuser or owner
DELETE: Delete User By Id (set isDelete = True)     # for superuser or owner
"""
class UserDetailView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return UserProfileSerializer
        return UserDetailSerializer


    def get(self, userId):
        try:
            user = CustomUser.objects.get(pk=userId)
            books = userBook.objects.filter(user=user, isSaved=True)
            movies = userMovie.objects.filter(user=user, isSaved=True)
            feeds = userFeed.objects.filter(user=user, isFollowed=True)
            user.books = books;
            user.movies = movies;
            user.feeds = feeds;
            serializer=self.get_serializer(instance=user)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get User Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, userId):
        try:
            user = get_object_or_404(CustomUser, pk=userId)
            serializer = self.get_serializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            return Response({"message": "Update User Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update User Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, userId):
        try:
            user = get_object_or_404(CustomUser, pk=userId)
            user.isDeleted = True
            user.updatedAt = timezone.now()
            user.save()
            return Response({"message": "Delete User Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete User Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
GET: Get All Users
POST: Create User (email, username)
"""
class UserListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListUserSerializer
        return UserCreateSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(isDeleted=False, is_active=True)


    def post(self, request): 
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        newUser = CustomUser.objects.get(email=serializer.data['email'])
        newToken = get_tokens(newUser)['access']

        send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt" )

        return Response(serializer.data, status=status.HTTP_201_CREATED)