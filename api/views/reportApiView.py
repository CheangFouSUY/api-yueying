from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.reportSerializers import *




""" For Admin(superuser)
GET: Get Report Detail By Id  # for any
PUT: Update Report By Id      # for superuser
DELETE: Delete Report By Id  # for superuser
"""
class ReportDetailView(generics.GenericAPIView):
    serializer_class = ReportDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Report Detail By Id
    @swagger_auto_schema(operation_summary="Get Report By Id")
    def get(self, request, reportId):
        try:
            report = get_object_or_404(Report, pk=reportId)
            serializer = self.serializer_class(instance=report)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Report Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Report Status By Id
    @swagger_auto_schema(operation_summary="Update Report By Id")
    def put(self, request, reportId):
        try:
            report = get_object_or_404(Report, pk=reportId)
            if not request.user.is_staff and request.user != report.createdBy:
                    return Response({"message": "Unauthorized for update report"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.serializer_class(instance=report, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Update Report Successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Report Failed"}, status=status.HTTP_400_BAD_REQUEST)


    # Delete Report By Id
    @swagger_auto_schema(operation_summary="Delete Reposrt By Id")
    def delete(self, request, reportId):
        try:
            report = get_object_or_404(Report, pk=reportId)
            if not request.user.is_staff and request.user != report.createdBy:
                return Response({"message": "Unauthorized for delete review"}, status=status.HTTP_401_UNAUTHORIZED)
            report.delete()
            return Response({"message": "Delete Report Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Report Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Report
"""
class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Get All Books")
    def post(self, request):
        try:
            user = request.user
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(createdBy=user, result=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create Report Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Reports
"""
class ReportListView(generics.ListAPIView):
    serializer_class = ListReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Reports
    @swagger_auto_schema(operation_summary="Get All Reports")
    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        feed = self.request.GET.get('feed')
        review = self.request.GET.get('review')
        result = self.request.GET.get('result')

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(reportFeed__title__icontains=term) | Q(reportReview__title__icontains=term) | Q(createdBy__username__icontains=term)
        if category is not None:
            filter &= Q(category=category)
        if feed is not None:
            filter &= Q(reportFeed=feed)
        if review is not None:
            filter &= Q(reportReview=review)
        if result is not None:
            filter &= Q(result=result)

        return Report.objects.filter(filter)
