from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions


from ..serializers.feedbackSerializers import *

from ..models.feeds import Feed


""" For Admin(superuser)
GET: Get Feedback Detail By Id  # for any
DELETE: Delete Feedback By Id  # for superuser
"""
class FeedbackDetailView(generics.GenericAPIView):
    serializer_class = FeedbackDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Feedback Detail By Id
    def get(self, request, feedbackId):
        try:
            feedback = get_object_or_404(Feed, pk=feedbackId)
            serializer = self.serializer_class(instance=feedback)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Feedback Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Feedback By Id
    def delete(self, request, feedbackId):
        try:
            feedback = get_object_or_404(Feedback, pk=feedbackId)
            feedback.delete()
            return Response({"message": "Delete Feedback Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Feedback Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Feedbacks
POST: Create Feedback
"""
class FeedbackListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListFeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListFeedbackSerializer
        return FeedbackCreateSerializer

    # Get All Feeds
    def get_queryset(self):
        return Feedback.objects.filter()

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
