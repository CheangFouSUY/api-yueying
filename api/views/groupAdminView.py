import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.groupSerializers import *
from ..serializers.groupRelationsSerializers import *
from ..serializers.feedSerializers import *
from ..serializers.userSerializers import *
from ..utils import *
from ..models.groups import Group
from ..models.userRelations import *
from ..models.feeds import *
from ..models.reviews import *
from ..models.groupRelations import *

'''
PUT:Set Group Admin -- admin and creator
PUT: Manage admin request
'''
class AdminSetView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Set Group Admin Role")
    def put(self,request,groupId,userId,result):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Set Group Admin Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            userApply = get_object_or_404(UserGroup, group=groupId, user=userId)
            adminrequest = get_object_or_404(GroupAdminRequest,group=groupId,user=userId)
            adminrequest_serial = AdminRequestSerializer(instance=adminrequest, data={'user':userId,'group':groupId,'result': result})
            adminrequest_serial.is_valid(raise_exception=True)
            adminrequest_serial.save(updatedAt=timezone.now())
            if result == 1:
                serializer = self.serializer_class(instance=userApply,data={'isAdmin':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Set Admin Successfully"
                return Response(data, status=status.HTTP_200_OK)
            elif result == 2:
                return Response({"message": "Request was decline"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

'''
PUT:Delete Group Admin -- only main admin
'''
class AdminDeleteView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Remove Group Admin Role")
    def put(self,request,groupId,userId):
        user = request.user
        isMainAdmin = UserGroup.objects.filter(group=groupId, user=user,isMainAdmin=True)

        if isMainAdmin:
            userDelete = get_object_or_404(UserGroup, group=groupId, user=userId,isAdmin=True)
            serializer = self.serializer_class(instance=userDelete,data={'isAdmin':False})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Delete Admin Successfully"
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

'''
PUT:Switch Main Admin - only creator/main admin
'''
class MainAdminSwitchView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer

    @swagger_auto_schema(operation_summary="Transfer Main Admin Role")
    def put(self,request,groupId,userId):
        user = request.user
        isMainAdmin = UserGroup.objects.filter(group=groupId, user=user,isMainAdmin=True).first()

        if isMainAdmin:
            userSwitch = get_object_or_404(UserGroup, group=groupId, user=userId)
            serializer = self.serializer_class(instance=userSwitch,data={'isMainAdmin':True})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            serializer1 = UserGroupDetailSerializer(instance=isMainAdmin, data={'isMainAdmin': False})
            serializer1.is_valid(raise_exception=True)
            serializer1.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Switch Main Admin Successfully"
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

### Feed Management ###
'''
PUT:Set Feed as Pinned and Unpin
'''
class PinnedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Pin Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Pin Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            isfeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if not isfeed.isPin:
                serializer = self.serializer_class(instance=isfeed,data={'isPin':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Pinned Feed Successfully"
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "Feed Already is Pinned"}, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

class UnpinFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Unpin Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)
        if userAdmin.isAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Unpin Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            isfeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if isfeed.isPin:
                serializer = self.serializer_class(instance=isfeed,data={'isPin':False})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Unpin Feed Successfully"
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "Feed is not pinned"}, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

'''
PUT:Set Feed as Featured and Unfeatured
'''
class FeaturedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Set Featured Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Feature Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            isfeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if not isfeed.isFeatured:
                serializer = self.serializer_class(instance=isfeed,data={'isFeatured':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Make Feed Featured Successfully"
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "Feed Already is Featured"}, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

class UnfeaturedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Remove Featured Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Unfeatured Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            isfeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if isfeed.isFeatured:
                serializer = self.serializer_class(instance=isfeed,data={'isFeatured':False})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                data = serializer.data
                data['message'] = "Unfeatured Feed Successfully"
                return Response(data, status=status.HTTP_200_OK)
            return Response({"message": "Feed is Not Featured"}, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

'''
DELETE:Delete Group Feed
'''
class GroupFeedDeleteView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Delete Group Feed By Id
    @swagger_auto_schema(operation_summary="Delete Group Feed By Id")
    def delete(self, request, groupId, feedId):
        user = get_object_or_404(UserGroup, group=groupId, user=request.user)
        feed = get_object_or_404(Feed, pk=feedId)
        if user.isAdmin or feed.createdBy == request.user: 
            if user.isBanned and not user.isMainAdmin: # Main Admin have all privilege
                if user.banDue > timezone.now():
                    return Response({"message": "Feature Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                user.isBanned = False

            isGroupfeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            isGroupfeed.delete()
            feed.delete()
            return Response({"message": "Delete Group Feed Successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)

'''
PUT:Banned Member
'''
class GroupMemberBanView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Ban Group Member, But Cannot Ban Group Main Admin")
    def put(self,request,groupId,userId):
        userAdmin = get_object_or_404(UserGroup, group=groupId, user=request.user)
        if userAdmin.isAdmin:
            userBan = get_object_or_404(UserGroup, group=groupId, user=userId)
            if userBan.isMainAdmin:  # Cannot ban group Main Admin
                return Response({"message": "Unable to Ban Main Admin", "data": serializer.data}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(instance=userBan, data={'isBanned': True})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now(),banDue=timezone.now() + timezone.timedelta(days=7))
            data = serializer.data
            data['message'] = "Ban Member Successfully"
            return Response(data, status=status.HTTP_200_OK)
        return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)
