from urllib import response
from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..utils import *
from ..models.books import Book

"""
Serializer class for Book Detail
"""
class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # need modification later on when implement with multiple models
        fields = ['id', 'isbn', 'title', 'description', 'img', 'thumbnail', 'author', 'publisher', 'year', 'category','createdAt']
        extra_kwargs = {
            'id': {'read_only': True},
            'thumbnail': {'read_only': True},
        }

"""
Serializer class for Book Profile (include rating, likes, dislikes)
"""
class BookProfileSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    response = serializers.CharField()
    isSave = serializers.BooleanField()
    isRate = serializers.BooleanField()
    score = serializers.FloatField()
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'description', 'img', 'thumbnail', 'author', 'publisher', 'year', 'category', 'rating', 'likes', 'dislikes','createdAt','response','isSave','isRate','score']
        extra_kwargs = {
            'id': {'read_only': True},
            'thumbnail': {'read_only': True},
        }


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'description', 'img', 'author', 'publisher', 'year', 'category']
        
    def validate(self, attrs):
        isbn = attrs.get('isbn', '')
        # isbn should be unique
        if Book.objects.filter(isbn=isbn).exists():
            raise ValidationError("Book isbn exists")
        return super().validate(attrs)



class ListBookSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    likes = serializers.IntegerField()
    dislikes = serializers.IntegerField()
    response = serializers.CharField()
    isSave = serializers.BooleanField()
    isRate = serializers.BooleanField()
    score = serializers.FloatField()
    
    class Meta:
        model = Book
        fields = ['id', 'isbn', 'title', 'description', 'thumbnail', 'author', 'publisher', 'category', 'rating', 'likes', 'dislikes','year','createdAt','response','isSave','isRate','score']