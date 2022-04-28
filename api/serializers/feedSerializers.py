from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.feeds import Feed

"""
Serializer class for Feed Detail
"""
class FeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'title', 'description', 'img', 'isPublic', 'isDeleted', 'createdBy', 'belongTo', 'createdAt', 'updatedAt']
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
        fields = ['title', 'description', 'img']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Feeds
"""
class ListFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'title', 'createdBy']

