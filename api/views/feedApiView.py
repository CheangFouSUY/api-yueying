from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.utils import timezone

from ..serializers.feedSerializers import *
from ..serializers.userRelationsSerializers import userFeedDetailSerializer
from ..utils import *
from ..models.feeds import Feed
from ..models.reviews import Review
from ..models.userRelations import userFeed


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
    def get(self, request, feedId):
        try:
            feed = get_object_or_404(Feed, pk=feedId)
            allReviews = Review.objects.filter(feed=feed)
            allUserFeeds = userFeed.objects.filter(feed=feed)
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.allReviews = allReviews
            serializer = self.get_serializer(instance=feed)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Feed Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Feed By Id
    def put(self, request, feedId):
        feed = get_object_or_404(Feed, pk=feedId)
        serializer = self.get_serializer(instance=feed, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updatedAt=timezone.now())
        return Response({"message": "Update Feed Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Feed By Id
    def delete(self, request, feedId):
        try:
            feed = get_object_or_404(Feed, pk=feedId)
            feed.delete()
            return Response({"message": "Delete Feed Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Feed Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Feeds
POST: Create Feed
"""
class FeedListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListFeedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListFeedSerializer
        return FeedCreateSerializer

    # Get All Feeds
    def get_queryset(self):
        allFeeds = Feed.objects.filter()
        for feed in allFeeds:
            allUserFeeds = userFeed.objects.filter(feed=feed)
            reviewers = Review.objects.filter(feed=feed).count()
            likes = allUserFeeds.filter(response='L').count()
            dislikes = allUserFeeds.filter(response='D').count()
            feed.likes = likes
            feed.dislikes = dislikes
            feed.reviewers = reviewers
        return allFeeds

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user, isPublic=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
PUT: userFeed relation, uses for response and follow
"""
class FeedReactionView(generics.GenericAPIView):
    serializer_class = userFeedDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, feedId):
        feed = get_object_or_404(Feed, pk=feedId)
        try:
            tmpUserFeed = userFeed.objects.get(feed=feedId, user=request.user)  # get one
        except userFeed.DoesNotExist:
            tmpUserFeed = None
        if tmpUserFeed:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserFeed, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(feed=feed, user=request.user, updatedAt=timezone.now())
            return Response({"message": "Update userFeed Successfully"}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(feed=feed, user=request.user)
            return Response({"message": "Add userFeed Successfully"}, status=status.HTTP_201_CREATED)