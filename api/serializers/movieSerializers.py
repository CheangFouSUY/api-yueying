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
        fields = ['id', 'title', 'description', 'img', 'thumbnail', 'director', 'actor', 'year', 'area','category','createdAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'thumbnail': {'read_only': True},
        }


"""
Serializer class for Movie Profile (include rating, likes, dislikes)
"""
class MovieProfileSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    isSave = serializers.BooleanField()
    response = serializers.CharField()
    isRate = serializers.BooleanField()
    score = serializers.FloatField()
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'img', 'thumbnail', 'director', 'actor', 'year', 'category','area', 'rating', 'likes', 'dislikes','createdAt','isSave','response','isRate','score']
        extra_kwargs = {
            'id': {'read_only': True},
            'thumbnail': {'read_only': True},
        }


"""
Serializer class for Creating Movie
"""
class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'img', 'director', 'actor', 'year','area', 'category']
        
    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Movies
"""
class ListMovieSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    isSave = serializers.BooleanField()
    response = serializers.CharField()
    isRate = serializers.BooleanField()
    score = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'thumbnail', 'director','actor', 'area','category', 'rating', 'likes', 'dislikes','year','createdAt','isSave','response','isRate','score']