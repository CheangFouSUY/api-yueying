from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions

from ..serializers.groupSerializers import *
from ..serializers.groupRelationsSerializers import *
from ..serializers.feedSerializers import *
from ..utils import *
from ..models.groups import Group
from ..models.userRelations import *
from ..models.feeds import *
from ..models.reviews import *
from ..models.groupRelations import *

""" For Admin(superuser)
GET: Get Group Detail By Id  # for any
PUT: Update Group By Id      # for superuser
DELETE: Delete Group By Id (set isDelete = True)     # for superuser
"""
class GroupDetailView(generics.GenericAPIView):
    serializer_class = GroupDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return GroupProfileSerializer
        return GroupDetailSerializer

    # Get Group Detail By Id
    def get(self, request, groupId):
        try:
            group = get_object_or_404(Group, pk=groupId)
            members = userGroup.objects.filter(group=groupId).count()
            group.members = members;
            serializer = self.serializer_class(instance=group)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)

        except:
            return Response({"message": "Get Group Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Group By Id
    def put(self, request, groupId):
        group = get_object_or_404(Group, pk=groupId)
        serializer = self.serializer_class(instance=group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updatedAt=timezone.now())
        return Response({"message": "Update Group Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Group By Id
    def delete(self, request, groupId):
        try:
            group = get_object_or_404(Group, pk=groupId)
            group.delete()
            return Response({"message": "Delete Group Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Group Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Groups
POST: Create Group
"""
class GroupListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListGroupSerializer
        return GroupCreateSerializer

    # Get All Groups

    def get_queryset(self):
        allGroups = Group.objects.filter()
        for group in allGroups:
            members = userGroup.objects.filter(group=group).count()
            group.members = members;
        return allGroups

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        group = get_object_or_404(Group, pk=serializer.data["id"])
        usergroup = userGroup(group=group, user=request.user,isAdmin=True)
        usergroup.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)

'''
Join group
'''
class joinGroupView(generics.GenericAPIView):
    serializer_class = UserGroupJoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self,request,groupId):
        group = get_object_or_404(Group, pk=groupId)
        data = {'user':request.user.id,'group':group.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

'''
GET: list feed 
POST: Create Feed in Group
'''

class GroupFeedListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #permission_classes = [permissions.IsGroupMemberOrReadOnly]  # need to modify permission

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListFeedSerializer
        return FeedCreateSerializer

    # Get All Group Feeds
    def get_queryset(self):
        group = self.kwargs['groupId']
        allFeeds = Feed.objects.filter(belongTo = group)
        for feed in allFeeds:
            allUserFeeds = userFeed.objects.filter(feed=feed)
            reviewers = Review.objects.filter(feed=feed).count()
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.reviewers = reviewers
        return allFeeds

    def post(self,request,groupId):
        user = request.user
        group = get_object_or_404(Group, pk=groupId)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user, isPublic=False ,belongTo=group)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

'''
Apply group admin 
'''

class GroupAdminApplyView(generics.ListCreateAPIView):
    serializer_class = GroupAdminSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupMember]  # need to modify permission，message of invalid permisson is define in permission.py

    def post(self,request,groupId):
        user = request.user
        group = get_object_or_404(Group, pk=groupId)
        '''
        isMember = userGroup.objects.filter(user = user)
        if not isMember:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)
        '''
        data = {'user':user.id,'group':group.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user,group=group)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



''' For Group Admin'''

'''
Set group admin -- admin and creator
'''
class AdminSetView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,userId):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            userApply = get_object_or_404(userGroup, group=groupId, user=userId)
            serializer = self.serializer_class(instance=userApply,data={'isAdmin':True})
            serializer.is_valid(raise_exception=True)
            serializer.save(isAdmin=True,updatedAt=timezone.now())
            return Response({"message": "Set Admin Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
Delete group admin -- only group creator
'''
class AdminDeleteView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupCreator]  # need to modify permission

    def put(self,request,groupId,userId):
        isCreator = Group.objects.filter(pk=groupId, createdBy=request.user)

        if isCreator:
            userDelete = get_object_or_404(userGroup, group=groupId, user=userId,isAdmin=True)
            serializer = self.serializer_class(instance=userDelete,data={'isAdmin':False})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            return Response({"message": "Delete Admin Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
Set feed as pinned and unpin
'''
class PinnedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            isfeed = get_object_or_404(groupFeed, group=groupId, feed=feedId)
            if not isfeed.isPin:
                serializer = self.serializer_class(instance=isfeed,data={'isPin':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())

            return Response({"message": "Pinned Feed Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

class UnpinFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            isfeed = get_object_or_404(groupFeed, group=groupId, feed=feedId)
            if isfeed.isPin:
                serializer = self.serializer_class(instance=isfeed,data={'isPin':False})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())

            return Response({"message": "Unpin Feed Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)


'''
Set feed as featured and unfeatured
'''
class FeaturedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            isfeed = get_object_or_404(groupFeed, group=groupId, feed=feedId)
            if not isfeed.isFeatured:
                serializer = self.serializer_class(instance=isfeed,data={'isFeatured':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())

            return Response({"message": "Make Feed Featured Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

class UnfeaturedFeedView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,feedId):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            isfeed = get_object_or_404(groupFeed, group=groupId, feed=feedId)
            if isfeed.isFeatured:
                serializer = self.serializer_class(instance=isfeed,data={'isFeatured':False})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())

            return Response({"message": "Unfeatured Feed Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
Delete group feed
'''
class GroupFeedDeleteView(generics.GenericAPIView):
    serializer_class = GroupFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    # Delete Group Feed By Id
    def delete(self, request, groupId, feedId):
        userAdmin = get_object_or_404(userGroup, group=groupId, user=request.user)
        if userAdmin.isAdmin:
            try:
                isgroupfeed = get_object_or_404(groupFeed, group=groupId, feed=feedId)
                feed = get_object_or_404(Feed, pk=feedId)
                isgroupfeed.delete()
                feed.delete()
                return Response({"message": "Delete Group Feed Successfully"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Delete Group Feed Failed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
Banned Member
'''
class GroupMemberBanView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupAdmin]  # need to modify permission，message of invalid permisson is define in permission.py

    def put(self,request,groupId,userId):
        userAdmin = get_object_or_404(userGroup, group=groupId, user=request.user)
        if userAdmin.isAdmin:
            userBan = get_object_or_404(userGroup, group=groupId, user=userId)
            serializer = self.serializer_class(instance=userBan, data={'isBanned': True})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now(),banDue=timezone.now() + timezone.timedelta(days=7))
            return Response({"message": "Ban Member Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)
