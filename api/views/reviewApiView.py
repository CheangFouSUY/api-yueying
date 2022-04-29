from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.utils import timezone

from ..serializers.reviewSerializers import *
from ..utils import *
from ..models.reviews import Review


""" For Admin(superuser)
GET: Get Feed Detail By Id  # for any
PUT: Update Feed By Id      # for superuser or owner
DELETE: Delete Feed By Id (set isDelete = True)     # for superuser or owner
"""
class ReviewDetailView(generics.GenericAPIView):
    serializer_class = ReviewDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Review Detail By Id
    def get(self, request, reviewId):
        try:
            review = get_object_or_404(Review, pk=reviewId)
            serializer = self.serializer_class(instance=review)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Review Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Review By Id
    def put(self, request, reviewId):
        review = get_object_or_404(Review, pk=reviewId)
        serializer = self.serializer_class(instance=review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updatedAt=timezone.now())
        return Response({"message": "Update Review Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Review By Id
    def delete(self, request, reviewId):
        try:
            review = get_object_or_404(Review, pk=reviewId)
            review.delete()
            return Response({"message": "Delete Review Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Review Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Reviews
POST: Create Review
"""
class ReviewListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListReviewSerializer
        return ReviewCreateSerializer

    # Get All Reviews
    def get_queryset(self):
        return Review.objects.filter()

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)