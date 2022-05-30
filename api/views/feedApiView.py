import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.feedSerializers import *
from ..serializers.userRelationsSerializers import UserFeedDetailSerializer
from ..models.feeds import Feed
from ..models.reviews import Review
from ..models.groups import Group
from ..models.userRelations import UserFeed, UserGroup


""" For Admin(superuser)
GET: Get Feed Detail By Id  # for any
PUT: Update Feed By Id      # for superuser or owner
DELETE: Delete Feed By Id (set isDelete = True)     # for superuser or owner
"""
class FeedDetailView(generics.GenericAPIView):
    serializer_class = FeedDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FeedProfileSerializer
        return FeedDetailSerializer

    # Get Feed Detail By Id
    @swagger_auto_schema(operation_summary="Get Feed Detail By Id")
    def get(self, request, feedId):
        try:
            feed = get_object_or_404(Feed, pk=feedId)
            allUserFeeds = UserFeed.objects.filter(feed=feed)
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.response = 'O'
            feed.isFollow = False
            if not request.user.is_anonymous:
                userfeed = UserFeed.objects.filter(user=self.request.user,feed=feed).first()
                if userfeed:
                    if userfeed.response == 'L':
                        feed.response = 'L'
                    if userfeed.response == 'D':
                        feed.response = 'D'
                    if userfeed.isFollowed:
                        feed.isFollow = True
            serializer = self.get_serializer(instance=feed)
            data = serializer.data
            data['message'] = "Get Feed Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Feed Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Feed By Id
    @swagger_auto_schema(operation_summary="Update Feed By Id")
    def put(self, request, feedId):
        try:
            feed = get_object_or_404(Feed, pk=feedId)
            if not request.user.is_staff and request.user != feed.createdBy:
                return Response({"message": "Unauthorized for update feed"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(instance=feed, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Feed Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Feed Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Feed By Id
    @swagger_auto_schema(operation_summary="Delete Feed By Id")
    def delete(self, request, feedId):
            feed = get_object_or_404(Feed, pk=feedId)
            if not feed.isPublic:
                group = get_object_or_404(Group, pk=feed.belongTo.id)

            admin = UserGroup.objects.filter(user=request.user,group=group.id).first()
            if not request.user.is_staff and request.user != feed.createdBy and not admin.isAdmin and not admin.isMainAdmin:
                return Response({"message": "Unauthorized for delete feed"}, status=status.HTTP_401_UNAUTHORIZED)
            feed.delete()
            return Response({"message": "Delete Feed Successfully"}, status=status.HTTP_200_OK)



"""
POST: Create Feed
"""
class FeedCreateView(generics.CreateAPIView):
    serializer_class = FeedCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    @swagger_auto_schema(operation_summary="Create Feed")
    def post(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(createdBy=user, isPublic=True)
            data = serializer.data

            feed = Feed.objects.get(pk=serializer.data["id"])
            userFeed = UserFeed(feed=feed,user=request.user)
            userFeed.isFollowed = True
            userFeed.save()

            data['message'] = "Create Feed Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create Feed Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Feeds
"""
class FeedListView(generics.ListAPIView):
    serializer_class = ListFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Feeds
    @swagger_auto_schema(operation_summary="Get All Feeds")
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')
        group = self.request.GET.get('belongTo')
        isPublic = self.request.GET.get('isPublic')
        followedBy = self.request.GET.get('followedBy')  # followedBy = userId
        createdBy = self.request.GET.get('createdBy')
        # by default, get feed return isPublic = True feed

    
        if isPublic is not None:
            isPublic = isPublic

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term)

        if group is not None:
            filter &= Q(belongTo=group)
            isPublic = False    # by Default if it has belongTo field, then it's not public anymore

        if followedBy is not None:
            filter &= Q(userfeed__user = followedBy, userfeed__isFollowed = True)

        if createdBy is not None:
            filter &= Q(createdBy = createdBy)
            
        if followedBy is None and createdBy is None and isPublic is not None:
            filter &= Q(isPublic=isPublic)

        allFeeds = Feed.objects.filter(filter).order_by('-createdAt')
        for feed in allFeeds:
            allUserFeeds = UserFeed.objects.filter(feed=feed)
            reviewers = Review.objects.filter(feed=feed).count()
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.reviewers = reviewers
            feed.response = 'O'
            feed.isFollow = False

            if not self.request.user.is_anonymous:
                userfeed = UserFeed.objects.filter(user=self.request.user,feed=feed).first()
                if userfeed:
                    if userfeed.response == 'L':
                        feed.response = 'L'
                    if userfeed.response == 'D':
                        feed.response = 'D'
                    if userfeed.isFollowed:
                        feed.isFollow = True

        if orderBy == 'l':
            orderBy = 'likes'
        elif orderBy == 'd':
            orderBy = 'dislikes'
        elif orderBy == 'r':
            orderBy = 'reviewers'
        else:
            return allFeeds

        ordered = sorted(allFeeds, key=operator.attrgetter(orderBy), reverse=True)

        return ordered

"""
PUT: UserFeed relation, uses for response and follow
"""
class FeedReactionView(generics.GenericAPIView):
    serializer_class = UserFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="React On Feed, ie. Likes, Dislikes")
    def put(self, request, feedId):
        feed = get_object_or_404(Feed, pk=feedId)
        if not feed.isPublic:
            group = feed.belongTo
            groupMember = UserGroup.objects.filter(group=group, user=request.user).first()
            if not groupMember or groupMember.banDue > timezone.now():
                return Response({"message": "Not group member/Banned Member,Unauthorized to react group feed"}, status=status.HTTP_401_UNAUTHORIZED)
            elif groupMember.banDue < timezone.now():
                groupMember.isBanned=False
                groupMember.save()
        
        try:
            tmpUserFeed = UserFeed.objects.get(feed=feedId, user=request.user)  # get one
        except UserFeed.DoesNotExist:
            tmpUserFeed = None
        if tmpUserFeed:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserFeed, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(feed=feed, user=request.user, updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update UserFeed Successfully"
            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(feed=feed, user=request.user)
            data = serializer.data
            data['message'] = "Add UserFeed Successfully"
            return Response(data, status=status.HTTP_201_CREATED)