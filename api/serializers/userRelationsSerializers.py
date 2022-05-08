from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.books import Book
from ..models.movies import Movie
from ..models.feeds import Feed
from ..models.reviews import Review
from ..models.users import CustomUser
from ..models.userRelations import *

class userBookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = userBook
        # need modification later on when implement with multiple models
        fields = ['book', 'user', 'response', 'isSaved', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'book': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


class userMovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = userMovie
        # need modification later on when implement with multiple models
        fields = ['movie', 'user', 'response', 'isSaved', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'movie': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


class userFeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = userFeed
        # need modification later on when implement with multiple models
        fields = ['feed', 'user', 'response', 'isFollowed', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'feed': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

class userReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = userReview
        # need modification later on when implement with multiple models
        fields = ['review', 'user', 'response', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'review': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


