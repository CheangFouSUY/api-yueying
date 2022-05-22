from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.reviews import Review

"""
Serializer class for Review Detail
"""
class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'description', 'img', 'isDeleted', 'createdBy', 'feed', 'book', 'movie', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'feed': {'read_only': True},
            'book': {'read_only': True},
            'movie': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Review Profile (include rating, likes, dislikes)
"""
class ReviewProfileSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    class Meta:
        model = Review
        fields = ['id', 'title', 'description', 'img', 'isDeleted', 'createdBy', 'feed', 'book', 'movie', 'createdAt', 'updatedAt', 'likes', 'dislikes']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'feed': {'read_only': True},
            'book': {'read_only': True},
            'movie': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Creating Review
"""
class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'description', 'img', 'feed', 'book', 'movie']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Reviews
"""
class ListReviewSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    class Meta:
        model = Review
        fields = ['id', 'title', 'description', 'createdBy', 'feed', 'book', 'movie', 'updatedAt', 'likes', 'dislikes','createdAt']

