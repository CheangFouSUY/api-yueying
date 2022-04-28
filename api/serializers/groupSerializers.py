from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.groups import Group

"""
Serializer class for Group Detail
"""
class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'groupName', 'description', 'category', 'createdBy']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
            'category': {'read_only': True}
        }


"""
Serializer class for Creating Group
"""
class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['groupName', 'description', 'category']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Groups
"""
class ListGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'groupName', 'description', 'category', 'createdBy']

