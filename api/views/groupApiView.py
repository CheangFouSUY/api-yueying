from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions

from ..serializers.groupSerializers import *
from ..utils import *
from ..models.groups import Group


""" For Admin(superuser)
GET: Get Group Detail By Id  # for any
PUT: Update Group By Id      # for superuser
DELETE: Delete Group By Id (set isDelete = True)     # for superuser
"""
class GroupDetailView(generics.GenericAPIView):
    serializer_class = GroupDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Group Detail By Id
    def get(self, request, groupId):
        try:
            group = get_object_or_404(Group, pk=groupId)
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
        return Group.objects.filter()

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)