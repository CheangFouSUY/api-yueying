from rest_framework import serializers
from ..models.report import Report


"""
Serializer class for Report Detail
"""

class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        #fields = ['id', 'title', 'description', 'reportFeed', 'reportReview','category','result','createdBy']
        extra_kwargs = {
            'id': {'read_only': True},
            'reportFeed': {'read_only': True},
            'reportReview': {'read_only': True},
            'result': {'read_only': True},
            'createdBy': {'read_only': True},
        }


"""
Serializer class for Creating Report
"""

class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['title', 'description','category','reportFeed', 'reportReview']

    def validate(self, attrs):
        return super().validate(attrs)

"""
Serializer class for Listing Report
"""
class ListReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        '__all__'
        #fields = ['id', 'title', 'description', 'reportFeed', 'reportReview','category','result','createdBy']