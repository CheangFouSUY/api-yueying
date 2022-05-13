from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.movies import Movie


"""
Serializer class for Movie Detail
"""
class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # need modification later on when implement with multiple models
        fields = ['id', 'title', 'description', 'img', 'thumbnail', 'director', 'actor', 'year', 'category']
        extra_kwargs = {
            'id': {'read_only': True},
        }


"""
Serializer class for Movie Profile (include rating, likes, dislikes)
"""
class MovieProfileSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'img', 'thumbnail', 'director', 'actor', 'year', 'category', 'rating', 'likes', 'dislikes']
        extra_kwargs = {
            'id': {'read_only': True},
        }


"""
Serializer class for Creating Movie
"""
class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'img', 'thumbnail', 'director', 'actor', 'year', 'category']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Movies
"""
class ListMovieSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'thumbnail', 'director', 'actor', 'category', 'rating', 'likes', 'dislikes']