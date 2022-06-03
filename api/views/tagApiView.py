import operator
from unicodedata import category
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.feedSerializers import *
from ..serializers.userRelationsSerializers import UserFeedDetailSerializer
from ..serializers.tagSerializers import *
from ..models.feeds import Feed
from ..models.reviews import Review
from ..models.groups import Group
from ..models.userRelations import UserFeed, UserGroup
from ..models.tags import Tag
from ..models.tagRelations import *

class TagDetailView(generics.GenericAPIView):
    serializer_class = TagDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Tag Detail By Id
    @swagger_auto_schema(operation_summary="Get Tag Detail By Id")
    def get(self, request, tagId):
        try:
            tag = get_object_or_404(Tag, pk=tagId)
            tag.feedCount = TagFeed.objects.filter(tag=tag).count()
            
            tag.isFollow = False
            
            if not request.user.is_anonymous:
                joinTag = UserTag.objects.filter(user=request.user,tag=tag).first()
                if joinTag:
                    tag.isFollow = True
            serializer = self.get_serializer(instance=tag)
            data = serializer.data
            data['message'] = "Get Tag Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Tag Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update tag By Id
    @swagger_auto_schema(operation_summary="Update Tag By Id")
    def put(self, request, tagId):
        try:
            tag = get_object_or_404(Tag, pk=tagId)
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for update tag"}, status=status.HTTP_401_UNAUTHORIZED)

            serializer = self.get_serializer(instance=tag, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Tag Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Tag Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Tag By Id
    @swagger_auto_schema(operation_summary="Delete Tag By Id")
    def delete(self, request, tagId):
            tag = get_object_or_404(Tag, pk=tagId)
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for delete tag."}, status=status.HTTP_401_UNAUTHORIZED)
            tag.delete()
            return Response({"message": "Delete Tag Successfully"}, status=status.HTTP_200_OK)

class TagCreateView(generics.CreateAPIView):
    serializer_class = TagCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Create Tag")
    def post(self, request):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for create tag"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Create Tag Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Create Tag Failed"}, status=status.HTTP_400_BAD_REQUEST)


class TagJoinView(generics.CreateAPIView):
    serializer_class = TagJoinSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Join Tag")
    def post(self, request):

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data

            data['message'] = "Join Tag Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        
class TagListView(generics.ListAPIView):
    serializer_class = TagListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Tags
    @swagger_auto_schema(operation_summary="Get All Tags")
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy') #feed,time
        search = self.request.GET.get('search')  #search in name
        joinedBy = self.request.GET.get('joinedBy')  # joinedBy = userId
        category = self.request.GET.get('category')
        
        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term)

        if joinedBy is not None:
            filter &= Q(usertag__user = joinedBy)

        if category == 'b':
            filter &= Q(category='b')
        elif category == 'm':
            filter &= Q(category='m')
        elif category == 'o':
            filter &= Q(category='o')

        allTags = Tag.objects.filter(filter).order_by('-createdAt')
        for tag in allTags:
            tag.feedCount = TagFeed.objects.filter(tag=tag).count()
            tag.isJoined = False

            if not self.request.user.is_anonymous:
                userTag = UserTag.objects.filter(user=self.request.user,tag=tag).first()
                if userTag:
                    tag.isJoined = True
                
        if orderBy == 'time':
            orderBy = 'createdAt'
        else:
            orderBy = 'feedCount'

        ordered = sorted(allTags, key=operator.attrgetter(orderBy),reverse=True)
        return ordered