from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.feeds import Feed
from .reviewSerializers import ReviewDetailSerializer

"""
Serializer class for Feed Detail
"""
class FeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'title', 'description', 'img', 'isPublic', 'belongTag','isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'isPublic': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Feed Profile (include rating, likes, dislikes)
"""
class FeedProfileSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    response = serializers.CharField()
    class Meta:
        model = Feed
        fields = ['id', 'title', 'description', 'img', 'isPublic', 'belongTag','isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt', 'likes', 'dislikes','response']
        extra_kwargs = {
            'id': {'read_only': True},
            'isPublic': {'read_only': True},
            'createdBy': {'read_only': True},
            'belongTo': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }


"""
Serializer class for Creating Feed
"""
class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id','title', 'description', 'img','belongTag']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Feeds
"""
class ListFeedSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    reviewers = serializers.IntegerField()
    response = serializers.CharField()
    class Meta:
        model = Feed
        fields = ['id', 'title', 'description','createdBy','isPublic', 'belongTag','likes', 'dislikes', 'reviewers','createdAt','response']


class ListGroupFeedSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    reviewers = serializers.IntegerField()
    isPin = serializers.IntegerField()
    isFeatured = serializers.IntegerField()
    response = serializers.CharField()
    class Meta:
        model = Feed
        fields = ['id', 'title','description','createdBy', 'likes', 'dislikes', 'reviewers','createdAt','isPin','isFeatured','response']