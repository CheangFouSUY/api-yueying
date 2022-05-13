from rest_framework import serializers
from ..models.feedbacks import Feedback


"""
Serializer class for Feedback Detail
"""

class FeedbackDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        #fields = ['id', 'title', 'description', 'createdBy']
        extra_kwargs = {
            'id': {'read_only': True},
            'createdBy': {'read_only': True},
        }


"""
Serializer class for Creating Feedback
"""

class FeedbackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['title', 'description', 'category']

    def validate(self, attrs):
        return super().validate(attrs)


"""
Serializer class for Listing Feedback
"""
class ListFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'createdBy']