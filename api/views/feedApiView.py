from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.utils import timezone

from ..serializers.feedSerializers import *
from ..utils import *
from ..models.feeds import Feed


""" For Admin(superuser)
GET: Get Feed Detail By Id  # for any
PUT: Update Feed By Id      # for superuser or owner
DELETE: Delete Feed By Id (set isDelete = True)     # for superuser or owner
"""
class FeedDetailView(generics.GenericAPIView):
    serializer_class = FeedDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Feed Detail By Id
    def get(self, request, feedId):
        try:
            feed = get_object_or_404(Feed, pk=feedId)
            serializer = self.serializer_class(instance=feed)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Feed Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Feed By Id
    def put(self, request, feedId):
        feed = get_object_or_404(Feed, pk=feedId)
        serializer = self.serializer_class(instance=feed, data=request.data)
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
            # Since the ReadSerializer does nested lookups
            # in multiple tables, only use it when necessary
            return ListFeedSerializer
        return FeedCreateSerializer

    # Get All Feeds
    def get_queryset(self):
        return Feed.objects.filter()

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user, isPublic=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)