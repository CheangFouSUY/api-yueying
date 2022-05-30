import operator
from tokenize import group
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
class SetRoleView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Set Group Role")
    def put(self,request,groupId,userId,role):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)
        targetUser = get_object_or_404(UserGroup, group=groupId, user=userId)

        if userAdmin.isAdmin or userAdmin.isMainAdmin:
                if role == 1:
                    if userAdmin.isMainAdmin:
                        targetUser.isMainAdmin = True
                        userAdmin.isMainAdmin = False
                        targetUser.save()
                        userAdmin.save()
                        return Response({"message": "Set Main Admin Successfully."}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": "Not Main Admin."}, status=status.HTTP_401_UNAUTHORIZED)
                
                if role == 2:
                    targetUser.isAdmin = True
                    request = GroupAdminRequest.objects.filter(group=groupId,user=targetUser.id).first()
                    targetUser.save()
                    if request:
                        request.result = 1
                        request.save()
                    return Response({"message": "Set Admin Successfully."}, status=status.HTTP_200_OK)
               
                if role == 3:
                    if targetUser.isAdmin and not userAdmin.isMainAdmin:
                        return Response({"message": "Not Main Admin."}, status=status.HTTP_401_UNAUTHORIZED)
                    targetUser.isAdmin = False
                    targetUser.isMainAdmin = False
                    targetUser.save()
                    return Response({"message": "Set Normal Member Successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not Group Admin."}, status=status.HTTP_401_UNAUTHORIZED)
            

### Feed Management ###
class SetPinFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Pin Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin or userAdmin.isMainAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Pin Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            groupFeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if not groupFeed.isPin: #if not pin
                groupFeed.isPin=True
                groupFeed.updatedAt=timezone.now()
                groupFeed.save()
                return Response({"message": "Pin Feed Succesfully"}, status=status.HTTP_200_OK)
            else: #if is pinned
                groupFeed.isPin=False
                groupFeed.updatedAt=timezone.now()
                groupFeed.save()
                return Response({"message": "Unpin Feed Succesfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_401_UNAUTHORIZED)


class SetFeaturedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Set Featured Feed In Group")
    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(UserGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin or userAdmin.isMainAdmin:
            if userAdmin.isBanned and not userAdmin.isMainAdmin: # Main Admin can do anything
                if userAdmin.banDue > timezone.now():
                    return Response({"message": "Feature Group Feed Failed, You Are Banned From This Action"}, status=status.HTTP_403_FORBIDDEN)
                # If bandue is now, set isBanned to fals
                userAdmin.isBanned = False

            groupFeed = get_object_or_404(GroupFeed, group=groupId, feed=feedId)
            if not groupFeed.isFeatured:
                groupFeed.isFeatured=True
                groupFeed.updatedAt=timezone.now()
                groupFeed.save()
                return Response({"message": "Make feed featured successfully"}, status=status.HTTP_200_OK)
            else:
                groupFeed.isFeatured=False
                groupFeed.updatedAt=timezone.now()
                groupFeed.save()
                return Response({"message": "Unfeatured feed successfully"}, status=status.HTTP_200_OK)
        else:
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
        if userAdmin.isAdmin or userAdmin.isMainAdmin:
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


