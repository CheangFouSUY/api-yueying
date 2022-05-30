from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.books import Book
from ..models.movies import Movie
from ..models.feeds import Feed
from ..models.reviews import Review
from ..models.users import CustomUser
from ..models.userRelations import *
from rest_framework.response import Response

class UserBookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        # need modification later on when implement with multiple models
        fields = ['book', 'user', 'response', 'isSaved', 'isRated', 'rateScore', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'book': {'read_only': True},
            'user': {'read_only': True},
            'isRated': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


class UserMovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovie
        # need modification later on when implement with multiple models
        fields = ['movie', 'user', 'response', 'isSaved', 'isRated', 'rateScore', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'movie': {'read_only': True},
            'user': {'read_only': True},
            'isRated': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


class UserFeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeed
        # need modification later on when implement with multiple models
        fields = ['feed', 'user', 'response', 'isFollowed', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'feed': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

class UserReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        # need modification later on when implement with multiple models
        fields = ['review', 'user', 'response', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'review': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


