from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from django.utils import timezone

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
    def get(self, request, reportId):
        try:
            report = get_object_or_404(Report, pk=reportId)
            serializer = self.serializer_class(instance=report)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Report Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Report Status By Id
    def put(self, request, reportId):
        report = get_object_or_404(Report, pk=reportId)
        serializer = self.serializer_class(instance=report, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Update Report Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Report By Id
    def delete(self, request, reportId):
        try:
            report = get_object_or_404(Report, pk=reportId)
            report.delete()
            return Response({"message": "Delete Report Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Report Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Reports
POST: Create Report
"""
class ReportListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListReportSerializer
        return ReportCreateSerializer

    # Get All Reports
    def get_queryset(self):
        return Report.objects.filter()

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(createdBy=user, result=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)