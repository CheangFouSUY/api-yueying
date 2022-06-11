from rest_framework import serializers
from ..utils import *
from ..models.feeds import Feed
from ..models.groupRelations import *
from ..models.userRelations import UserGroup


class GroupFeedDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupFeed
        fields = ['feed', 'group', 'createdAt', 'updatedAt']
        extra_kwargs = {
            'feed': {'read_only': True},
            'group': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

class UserGroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'
        extra_kwargs = {
            'group': {'read_only': True},
            'user': {'read_only': True},
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

class UserGroupJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ['user','group','createdAt']

    def validate(self, attrs):
        return super().validate(attrs)

class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupAdminRequest
        fields = '__all__'

    extra_kwargs = {
        'group': {'read_only': True},
        'user': {'read_only': True},
        'createdAt': {'read_only': True},
        'updatedAt': {'read_only': True},
    }

