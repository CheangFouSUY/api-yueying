import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.reviewSerializers import *
from ..serializers.userRelationsSerializers import UserReviewDetailSerializer
from ..utils import *
from ..models.reviews import Review
from ..models.feeds import Feed
from ..models.userRelations import *
from ..api_throttles import *


""" For Admin(superuser)
GET: Get Review Detail By Id  # for any
PUT: Update Review By Id      # for superuser or owner
DELETE: Delete Review By Id (set isDelete = True)     # for superuser or owner
"""
class ReviewDetailView(generics.GenericAPIView):
    serializer_class = ReviewDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ReviewProfileSerializer
        return ReviewDetailSerializer

    # Get Review Detail By Id
    @swagger_auto_schema(operation_summary="Get Review By Id")
    def get(self, request, reviewId):
        try:
            review = get_object_or_404(Review, pk=reviewId)
            allUserReviews = UserReview.objects.filter(review=review)
            likes = allUserReviews.filter(response='L').count()
            dislikes = allUserReviews.filter(response='D').count()
            review.likes = likes
            review.dislikes = dislikes
            review.response = 'O'
            if not request.user.is_anonymous:
                userreview = UserReview.objects.filter(user=self.request.user,review=review).first()
                if userreview:
                    if userreview.response == 'L':
                        review.response = 'L'
                    if userreview.response == 'D':
                        review.response = 'D'
            serializer = self.get_serializer(instance=review)
            data = serializer.data
            data['message'] = "Get Review Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Review Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Review By Id
    @swagger_auto_schema(operation_summary="Update Review By Id")
    def put(self, request, reviewId):
        try:
            review = get_object_or_404(Review, pk=reviewId)
            if not request.user.is_staff and request.user != review.createdBy:
                return Response({"message": "Unauthorized for update review"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(instance=review, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Review Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Review Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Review By Id
    @swagger_auto_schema(operation_summary="Delete Review By Id")
    def delete(self, request, reviewId):
        try:
            review = get_object_or_404(Review, pk=reviewId)
            if not request.user.is_staff and request.user != review.createdBy:
                return Response({"message": "Unauthorized for delete review"}, status=status.HTTP_401_UNAUTHORIZED)
            review.delete()
            return Response({"message": "Delete Review Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Review Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Review
"""
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Create Review")
    def post(self, request):
        feed = request.data.get('feed', '') or None
        feed = Feed.objects.filter(pk=feed).first()
        if feed:
            if not feed.isPublic:
                group = feed.belongTo
                groupMember = UserGroup.objects.filter(group=group,user=request.user).first()
                if not groupMember:
                    return Response({"message": "Not group member,Unauthorized to react group feed"}, status=status.HTTP_401_UNAUTHORIZED)
                elif groupMember.isBanned:
                    if groupMember.banDue > timezone.now():
                        return Response({"message": "Banned Member,Unauthorized to react group feed"}, status=status.HTTP_401_UNAUTHORIZED)
                    elif groupMember.banDue < timezone.now():
                        groupMember.isBanned=False
                        groupMember.save()
        try:
            user = request.user
            data = request.data
            data.feed = request.data.get('feed', '') or None
            data.book = request.data.get('book', '') or None
            data.movie = request.data.get('movie', '') or None
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(createdBy=user)
            data = serializer.data
            data['message'] = "Create Review Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create Review Failed"}, status=status.HTTP_400_BAD_REQUEST)



"""
GET: Get All Reviews
"""
class ReviewListView(generics.ListAPIView):
    serializer_class = ListReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Reviews
    @swagger_auto_schema(operation_summary="Get All Reviews")
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')
        searchName = self.request.GET.get('searchName')
        feed = self.request.GET.get('feed')
        book = self.request.GET.get('book')
        movie = self.request.GET.get('movie')

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(description__icontains=term) | Q(createdBy__username__icontains=term) | Q(feed__title__icontains=term) 

        if searchName is not None:
            searchTerms = searchName.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term)

        if feed is not None:
            filter &= Q(feed=feed)
        if book is not None:
            filter &= Q(book=book)
        if movie is not None:
            filter &= Q(movie=movie)

            
        allReviews = Review.objects.filter(filter).order_by('-createdAt')
        for review in allReviews:
            allUserReviews = UserReview.objects.filter(review=review)
            likes = allUserReviews.filter(response='L').count()
            dislikes = allUserReviews.filter(response='D').count()
            review.likes = likes
            review.dislikes = dislikes
            review.response = 'O'

            if not self.request.user.is_anonymous:
                userreview = UserReview.objects.filter(user=self.request.user,review=review).first()
                if userreview:
                    if userreview.response == 'L':
                        review.response = 'L'
                    if userreview.response == 'D':
                        review.response = 'D'

        if orderBy == 'd':
            orderBy = 'dislikes'
        elif orderBy == 'l':
            orderBy = 'likes'
        else:
            return allReviews

        ordered = sorted(allReviews, key=operator.attrgetter(orderBy), reverse=True)

        return ordered


"""
PUT: UserReview relation, uses for response
"""
class ReviewReactionView(generics.GenericAPIView):
    serializer_class = UserReviewDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="React On Review, ie. Likes, Dislikes")
    def put(self, request, reviewId):
        review = get_object_or_404(Review, pk=reviewId)
        if review.feed:
            feed = get_object_or_404(Feed, pk=review.feed.id)
            if not feed.isPublic:
                group = feed.belongTo
                groupMember = UserGroup.objects.filter(group=group,user=request.user).first()
                if not groupMember:
                    return Response({"message": "Not group member,Unauthorized to react group feed's review"}, status=status.HTTP_401_UNAUTHORIZED)
                elif groupMember.isBanned:
                    if groupMember.banDue > timezone.now():
                        return Response({"message": "Banned Member,Unauthorized to react group feed's review"}, status=status.HTTP_401_UNAUTHORIZED)
                    elif groupMember.banDue < timezone.now():
                        groupMember.isBanned=False
                        groupMember.save()
        try:
            tmpUserReview = UserReview.objects.get(review=reviewId, user=request.user)  # get one
        except UserReview.DoesNotExist:
            tmpUserReview = None
        if tmpUserReview:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserReview, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(review=review, user=request.user, updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update UserReview Successfully"
            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(review=review, user=request.user)
            data = serializer.data
            data['message'] = "Add UserReview Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
