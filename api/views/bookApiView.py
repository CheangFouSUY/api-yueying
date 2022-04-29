from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions

from ..serializers.bookSerializers import *
from ..utils import *
from ..models.books import Book


""" For Admin(superuser)
GET: Get Book Detail By Id  # for any
PUT: Update Book By Id      # for superuser
DELETE: Delete Book By Id (set isDelete = True)     # for superuser
"""
class BookDetailView(generics.GenericAPIView):
    serializer_class = BookDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get Book Detail By Id
    def get(self, request, bookId):
        try:
            book = get_object_or_404(Book, pk=bookId)
            serializer = self.serializer_class(instance=book)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Book Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Book By Id
    def put(self, request, bookId):
        book = get_object_or_404(Book, pk=bookId)
        serializer = self.serializer_class(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updatedAt=timezone.now())
        return Response({"message": "Update Book Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Book By Id
    def delete(self, request, bookId):
        try:
            book = get_object_or_404(Book, pk=bookId)
            book.delete()
            return Response({"message": "Delete Book Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Book Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Books
POST: Create Book
"""
class BookListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListBookSerializer
        return BookCreateSerializer

    # Get All Books
    def get_queryset(self):
        return Book.objects.filter()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)