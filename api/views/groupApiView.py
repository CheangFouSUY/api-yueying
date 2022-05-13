import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.db.models import Q

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

"""
GET : Get a group by Id
PUT: Update Group By Id 
DELETE: Delete Group By Id
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
            group.members = members
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
            group = get_object_or_404(Group, pk=groupId,createdBy=request.user)
            group.delete()
            return Response({"message": "Delete Group Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Group Failed,Probably Not Group Creator"}, status=status.HTTP_400_BAD_REQUEST)

'''
POST:Create Group
'''
class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        #add userGroup
        group = get_object_or_404(Group, pk=serializer.data["id"])
        usergroup = userGroup(group=group, user=request.user,isAdmin=True,isMainAdmin=True)
        usergroup.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)


'''
POST/DELETE: Join and leave group
'''
class JoinLeaveGroupView(generics.GenericAPIView):
    serializer_class = UserGroupJoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self,request,groupId):
        group = get_object_or_404(Group, pk=groupId)
        data = {'user':request.user.id,'group':group.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, groupId):
        user = request.user
        isMember = userGroup.objects.filter(group=groupId, user=user)

        if isMember:
            if not isMember.isMainAdmin:
                isMember.delete()
                return Response({"message": "Leave Group Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Leave Group Failed,You Are Main Admin Of The Group"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Leave Group Failed,Not Group Member"}, status=status.HTTP_403_FORBIDDEN)

#################################### For members ####################################

'''
POST: Create Feed in Group
'''
class GroupFeedCreateView(generics.CreateAPIView):
    serializer_class = FeedCreateSerializer

    def post(self,request,groupId):
        user = request.user
        isMember = userGroup.objects.filter(group=groupId, user=user)
        if isMember:
            group = get_object_or_404(Group, pk=groupId)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(createdBy=user, isPublic=False ,belongTo=group)

            # add groupFeed
            group = get_object_or_404(Group, pk=groupId)
            feed = get_object_or_404(Feed, pk=serializer.data["id"])
            groupfeed = groupFeed(group=group, feed=feed)
            groupfeed.save()
            print(groupfeed)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Not Group Member."}, status=status.HTTP_403_FORBIDDEN)


'''
POST:Request Group Admin 
'''
class GroupAdminRequestView(generics.ListCreateAPIView):
    serializer_class = AdminRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsGroupMember]  # need to modify permission，message of invalid permisson is define in permission.py

    def post(self,request,groupId):
        try:
            user = request.user
            isMember = userGroup.objects.filter(group=groupId, user=user)
            if isMember:
                data = {'user':user.id,'group':groupId}
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({"message": "Apply Group Admin Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Apply group admin Failed,Not Group Member"},status=status.HTTP_403_FORBIDDEN)


############################## For Group Admin ##################################
### Admin Management ###
'''
PUT:Set Group Admin -- admin and creator
PUT: Manage admin request
'''
class AdminSetView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self,request,groupId,userId,result):
        userAdmin = get_object_or_404(userGroup, group=groupId,user=request.user)

        if userAdmin.isAdmin:
            userApply = get_object_or_404(userGroup, group=groupId, user=userId)
            request = get_object_or_404(groupAdminRequest,group=groupId,user=userId)
            request_serial = AdminRequestSerializer(instance=request, data={'user':userId,'group':groupId,'result': result})
            request_serial.is_valid(raise_exception=True)
            request_serial.save(updatedAt=timezone.now())
            if result == 1:
                serializer = self.serializer_class(instance=userApply,data={'isAdmin':True})
                serializer.is_valid(raise_exception=True)
                serializer.save(updatedAt=timezone.now())
                return Response({"message": "Set Admin Successfully", "data": serializer.data},status=status.HTTP_200_OK)
            elif result == 2:
                return Response({"message": "Request was decline"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
PUT:Delete Group Admin -- only group creator
'''
class AdminDeleteView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self,request,groupId,userId):
        user = request.user
        isMainAdmin = userGroup.objects.filter(group=groupId, user=user,isMainAdmin=True)

        if isMainAdmin:
            userDelete = get_object_or_404(userGroup, group=groupId, user=userId,isAdmin=True)
            serializer = self.serializer_class(instance=userDelete,data={'isAdmin':False})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            return Response({"message": "Delete Admin Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

'''
PUT:Switch Main Admin - only creator/main admin
'''
class MainAdminSwitchView(generics.GenericAPIView):
    serializer_class = UserGroupDetailSerializer

    def put(self,request,groupId,userId):
        user = request.user
        isMainAdmin = userGroup.objects.filter(group=groupId, user=user,isMainAdmin=True).first()

        if isMainAdmin:
            userSwitch = get_object_or_404(userGroup, group=groupId, user=userId)
            serializer = self.serializer_class(instance=userSwitch,data={'isMainAdmin':True})
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            serializer1 = UserGroupDetailSerializer(instance=isMainAdmin, data={'isMainAdmin': False})
            serializer1.is_valid(raise_exception=True)
            serializer1.save(updatedAt=timezone.now())
            return Response({"message": "Switch Main Admin Successfully", "data": serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Permission."}, status=status.HTTP_403_FORBIDDEN)

### Feed Management ###
'''
PUT:Set Feed as Pinned and Unpin
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
PUT:Set Feed as Featured and Unfeatured
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
DELETE:Delete Group Feed
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
PUT:Banned Member
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


################################ Show ######################################
### Outside ###
'''
GET: Sort by Category (members in descending order)
'''
class GroupbyCategoryView(generics.ListCreateAPIView):
    serializer_class = ListGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        type = self.kwargs['category']
        allGroups = Group.objects.filter(category=type)
        for group in allGroups:
            members = userGroup.objects.filter(group=group).count()
            group.members = members

        return ordered

'''
GET: Show group join by user
'''
class ShowUserGroupView(generics.ListCreateAPIView):
    serializer_class = ListGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        allGroups = Group.objects.filter(usergroup__user=self.request.user)
        for group in allGroups:
            members = userGroup.objects.filter(group=group).count()
            group.members = members
        ordered = sorted(allGroups, key=operator.attrgetter('members'), reverse=True)
        return ordered

### Inside Group ###
'''
GET : Show/Search Group Feed
'''
class GroupFeedListView(generics.ListAPIView):
    serializer_class = ListFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Group Feeds
    def get_queryset(self):
        group = self.kwargs['groupId']
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')

        filter = Q()
        filter &= Q(belongTo = group)

        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term)

        allFeeds = Feed.objects.filter(filter)
        for feed in allFeeds:
            allUserFeeds = userFeed.objects.filter(feed=feed)
            reviewers = Review.objects.filter(feed=feed).count()
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.reviewers = reviewers
            pin = groupFeed.objects.filter(feed=feed,group=group,isPin = True)
            if pin:
                feed.isPin = 0
            else:
                feed.isPin = 1
        ordered = sorted(allFeeds, key=operator.attrgetter('isPin','updatedAt'))
        return ordered

################################ Query ######################################
'''
GET:Show/Search Group
'''
class GroupListView(generics.ListAPIView):
    serializer_class = ListGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Groups
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter |= Q(groupName__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term)

        if category is not None:
            filter &= Q(category=category)


        allGroups = Group.objects.filter(filter)
        for group in allGroups:
            members = userGroup.objects.filter(group=group).count()
            group.members = members
        ordered = sorted(allGroups, key=operator.attrgetter('members'), reverse=True)
        return ordered

'''
GET:Show/Search Member (prior main admin and other admin) (only member can search?)
'''
class GroupMemberView(generics.ListAPIView):
    serializer_class = ListUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        group = self.kwargs['groupId']
        search = self.request.GET.get('search')

        filter = Q()
        filter &= Q(usergroup__group=group)
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(username__icontains=term)

        allMember = CustomUser.objects.filter(filter)
        for member in allMember:
            admin = userGroup.objects.filter(user=member, group=group).first()
            if admin.isMainAdmin:
                member.isAdmin = 0
            elif admin.isAdmin:
                member.isAdmin = 1
            else:
                member.isAdmin = 2
        ordered = sorted(allMember, key=operator.attrgetter('isAdmin'))
        return ordered

'''
GET:Show Admin Request
'''
class ShowRequestView(generics.ListCreateAPIView):
    serializer_class = AdminRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        group = self.kwargs['groupId']
        allRequest = groupAdminRequest.objects.filter(group=group,result=0)
        return allRequest

