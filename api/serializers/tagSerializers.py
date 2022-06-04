from asyncore import read
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.models.userRelations import UserTag
from ..utils import *
from ..models.feeds import Feed
from ..models.tags import Tag
from ..models.tagRelations import *


class TagDetailSerializer(serializers.ModelSerializer):
    feedCount = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=150)
    category = serializers.CharField(max_length=1)
    isJoined = serializers.BooleanField()

    class Meta:
        model = Tag
        fields = ['id','title','category','isJoined','feedCount','createdAt','updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'feedCount': {'allow_null': True},
            'isJoined':{'read_only':True},
            'category': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

class TagJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = ['user','tag']


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','title','category']

    def validate(self, attrs):
        return super().validate(attrs)

class TagListSerializer(serializers.ModelSerializer):
    feedCount = serializers.IntegerField()
    isJoined = serializers.BooleanField()
    class Meta:
        model = Tag
        fields = ['id','title','category','feedCount','isJoined','createdAt','updatedAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'category': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }