from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.contrib.auth.hashers import make_password,check_password
from drf_yasg.utils import swagger_auto_schema

import jwt
from ..serializers.userSerializers import *
from ..utils import get_tokens, send_smtp
from ..models.users import CustomUser
from ..models.userRelations import *
import re



def UserValidation(email,username,password,password2,mode):
    string = "~!@#$%^&*()_+-*/<>,.[]\/"
    if mode == 0:
        if CustomUser.objects.filter(email=email).exists():
            return 1001

        if CustomUser.objects.filter(username=username).exists():
            return 1002

    if password != password2:
        return 1003
    
    if len(password) < 8:
        return 1004

    testSym = re.search(r"\W",password)
    testNum = re.search(r'\d',password)
    my_re = re.compile(r'[A-Za-z]',re.S)
    testAl = re.findall(my_re,password)

    if testSym and testNum and testAl:
        return 200
    else:
        return 1004

    
"""
POST: Register
"""
class UserRegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(operation_summary="Register New User")
    def post(self, request):
        try:
            email = request.data.get('email', '')
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            password2 = request.data.get('password2', '')

            code = UserValidation(email,username,password,password2,0)

            if code == 1001:
                return Response({"message": "Email is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1002:
                return Response({"message": "Username is taken.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1003:
                return Response({"message": "Password not match.","code":code}, status=status.HTTP_400_BAD_REQUEST)
            elif code == 1004:
                return Response({"message": "Password too simple.","code":code}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            newUser = CustomUser.objects.get(email=serializer.data['email'])
            newToken = get_tokens(newUser)['access']

            send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
            data = serializer.data
            data['message'] = "Register Account Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Register Account Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
GET: Activate Account
"""
class UserActivateView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserActivateSerializer

    @swagger_auto_schema(operation_summary="Activate User Account")
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
            return Response({"message": "Activation Code Expire"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Request Password
"""
class RequestPasswordView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RequestPasswordSerializer

    @swagger_auto_schema(operation_summary="Request New Password Through Email")
    def post(self, request):
        try: 
            email = request.data.get('email', '')
            username = request.data.get('username', '')

            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                if not user.username == username: # incase the username is not the same as email
                    return Response({"message": "Invalid Username or Email"}, status=status.HTTP_400_BAD_REQUEST)
                newToken = get_tokens(user)['access']
                send_smtp(user, request, newToken, "Reset Password for YueYing", "reset_email.txt", False)
                return Response({"message": "Please check your email for futher info."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User not exists."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Failed to Request Password"}, status=status.HTTP_400_BAD_REQUEST)

"""
GET: Validate Token for Reset Password
"""
class ResetPasswordTokenValidateView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(operation_summary="Validate Token Of Request Password")
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = CustomUser.objects.get(id=payload['user_id'])
            authToken = get_tokens(user)
            # return Response(authToken, status=status.HTTP_200_OK)
            return Response({"tokens": authToken, "message": "Reset Link is Valid"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"message": "Reset Link Expire"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

"""
PUT: Reset Password (for authenticated user only)
"""
class ResetPasswordEmailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        # try:
        serializer = self.get_serializer(data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.updatePassword()
            # When update success, should terminate the token, so it cannot be used again
            # user = self.request.user
            # user = authenticate(username=user.username, password=request.data.get('password', ''))
            # token = get_tokens(user)

            return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
        # except:
        #     return Response({"message": "Password Reset Failed"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordbyOldpasswordView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordByPasswordSerializer

    @swagger_auto_schema(operation_summary="Reset Password Through Old Password")
    def put(self, request):
        try:
            oldpassword = request.data['oldpassword']
            username = request.user.username
            user = CustomUser.objects.get(username=username)
            result = user.check_password(oldpassword)
            if result:
                newpassword = request.data['newpassword']
                newpassword2 = request.data['newpassword2']
                code = UserValidation(None,None,newpassword,newpassword2,1)
                
                if code == 1003:
                    return Response({"message": "Password not match.","code":code}, status=status.HTTP_400_BAD_REQUEST)
                elif code == 1004:
                    return Response({"message": "Password too simple.","code":code}, status=status.HTTP_400_BAD_REQUEST)

                serializer = self.get_serializer(data=request.data, user=self.request.user)
                serializer.is_valid()
                serializer.updatePassword()
                    # When update success, should terminate the token, so it cannot be used again
                return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Old Password Is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Password Reset Failed"}, status=status.HTTP_400_BAD_REQUEST)

class RequestQuestionView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RequestQuestionSerializer

    @swagger_auto_schema(operation_summary="Request For Security Question By Username")
    def get(self, request):
        username = request.GET.get('username')
        user = CustomUser.objects.filter(username=username)
        if user.exists():
            user = user[0]
            data = {}
            data['securityQuestion'] = user.securityQuestion
            data["message"] = "Get Question Successfully"
            return Response(data, status=status.HTTP_200_OK)
        return Response ({"message": "User not existed"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordbyQuestionView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordByQuestionSerializer

    @swagger_auto_schema(operation_summary="Reset Password Through Answering Security Question")
    def put(self, request):
            username = request.data['username']  #需要给username,不是自动拿request.user
            questionNo = int(request.data['securityQuestion'])
            answer = request.data['securityAnswer'].lower()
            answer = make_password(answer,"a","pbkdf2_sha1")
            user = get_object_or_404(CustomUser, username=username)

            correctAns = user.securityAnswer
            correctNo = user.securityQuestion

            if questionNo == correctNo:
                if correctAns == answer:
                    newpassword = request.data['password']
                    newpassword2 = request.data['password2']
                    code = UserValidation(None,None,newpassword,newpassword2,1)
                    
                    if code == 1003:
                        return Response({"message": "Password not match.","code":code}, status=status.HTTP_400_BAD_REQUEST)
                    elif code == 1004:
                        return Response({"message": "Password too simple.","code":code}, status=status.HTTP_400_BAD_REQUEST)

                    serializer = self.get_serializer(data=request.data, user=user)
                    serializer.is_valid()
                    serializer.updatePassword()
                        # When update success, should terminate the token, so it cannot be used again
                    return Response({"message": "Password Reset Successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Security Answer Is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Security Question Is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)

class ResetSecurityQuestionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetQuestionSerializer

    @swagger_auto_schema(operation_summary="Reset Security Question And Answer")
    def put(self, request):
        try:
            password = request.data['password']
            username = request.user.username
            user = CustomUser.objects.get(username=username)
            result = user.check_password(password)

            if result:
                securityAnswer = request.data['securityAnswer']
                securityQuestion = request.data['securityQuestion']
                securityAnswer = securityAnswer.lower()
                user.securityAnswer = make_password(securityAnswer, "a", "pbkdf2_sha1")
                user.securityQuestion = securityQuestion
                user.updatedAt = timezone.now()
                user.save()
                return Response({"message": "Security Question Reset Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Password Is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Security Question Reset Failed"}, status=status.HTTP_400_BAD_REQUEST)
"""
POST: Login
"""
class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_summary="User Login")
    def post(self, request):

        username = request.data['username']
        data = {}
        data['password'] = request.data['password']

        filter = Q(email=username) | Q(username=username)
        user = CustomUser.objects.filter(filter)
        if not user.exists():
            return Response({"message": "Invalid credentials, try again"},  status= status.HTTP_400_BAD_REQUEST)
        
        user = user[0]
        data['username'] = user.username

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)


        data = serializer.data
        data['id'] = user.id
        data['firstName'] = user.firstName or None
        data['lastName'] = user.lastName or None
        data['thumbnail'] = user.thumbnail or None
        data['gender'] = user.gender or None
        data['is_staff'] = user.is_staff
        data['dob'] = user.dob or None
        data['message'] = "Login Successfully"
        return Response(data,  status= status.HTTP_200_OK)

"""
POST: Logout
"""
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    @swagger_auto_schema(operation_summary="User Logout")
    def post(self, request):
        try:
            # apparently no need to delete access token on logout, it should time out quickly enough anyway.
            # https://medium.com/devgorilla/how-to-log-out-when-using-jwt-a8c7823e8a6
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({"message": "Logout Successfully"}, status=status.HTTP_204_NO_CONTENT)
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

    @swagger_auto_schema(operation_summary="Get User Detail By Id")
    def get(self, request, userId):
        try:
            user = CustomUser.objects.get(pk=userId)
            serializer=self.get_serializer(instance=user)
            data = serializer.data
            data['message'] = "Get User Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get User Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Update User By Id")
    def put(self, request, userId):
        try:
            user = get_object_or_404(CustomUser, pk=userId)
            if not request.user.is_staff and request.user != user:
                return Response({"message": "Unauthorized for update user"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update User Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update User Failed"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete User By Id")
    def delete(self, request, userId):
        try:
            user = get_object_or_404(CustomUser, pk=userId)
            if not request.user.is_staff and request.user != user:
                return Response({"message": "Unauthorized for delete user"}, status=status.HTTP_401_UNAUTHORIZED)
            user.isDeleted = True
            user.updatedAt = timezone.now()
            user.save()
            return Response({"message": "Delete User Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete User Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
POST: Create User (email, username)
"""
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Create User")
    def post(self, request): 
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for create user"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            newUser = CustomUser.objects.get(email=serializer.data['email'])
            newToken = get_tokens(newUser)['access']

            send_smtp(newUser, request, newToken, "Activate Account", "register_email.txt", True)
            
            data = serializer.data
            data['message'] = "Create User Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create User Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Users
"""
class UserListView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get All Users")
    def get_queryset(self):
        search = self.request.GET.get('search')
        isDeleted = self.request.GET.get('isDelete')
        isActive = self.request.GET.get('isActive')
        gender = self.request.GET.get('gender')
        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(username__icontains=term) | Q(firstName__icontains=term) | Q(lastName__icontains=term) | Q(email__icontains=term)

        if isDeleted is None:
            isDeleted = False

        if isActive is None:
            isActive = True

        if gender is not None:
            filter &= Q(gender=gender)

        filter &= Q(is_active=isActive)
        filter &= Q(isDeleted=isDeleted)

        return CustomUser.objects.filter(filter)
