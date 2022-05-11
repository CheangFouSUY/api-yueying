from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions

from ..serializers.bookSerializers import *
from ..serializers.userRelationsSerializers import userBookDetailSerializer
from ..utils import *
from ..models.books import Book
from ..models.userRelations import userBook


""" For Admin(superuser)
GET: Get Book Detail By Id  # for any
PUT: Update Book By Id      # for superuser
DELETE: Delete Book By Id (set isDelete = True)     # for superuser
"""
class BookDetailView(generics.GenericAPIView):
    serializer_class = BookDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BookProfileSerializer
        return BookDetailSerializer

    # Get Book Detail By Id
    def get(self, request, bookId):
        try:
            book = get_object_or_404(Book, pk=bookId)
            allUserBooks = userBook.objects.filter(book=book)
            rating = allUserBooks.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserBooks.filter(response='L').count()
            dislikes = allUserBooks.filter(response='D').count()
            # rateScore using aggregate method, will return dic, and name is field__avg, value=null if no result
            book.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            book.likes = likes
            book.dislikes = dislikes
            serializer = self.get_serializer(instance=book)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Book Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Book By Id
    def put(self, request, bookId):
        book = get_object_or_404(Book, pk=bookId)
        serializer = self.get_serializer(instance=book, data=request.data)
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
        allBooks = Book.objects.filter()
        for book in allBooks:
            allUserBooks = userBook.objects.filter(book=book)
            rating = allUserBooks.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserBooks.filter(response='L').count()
            dislikes = allUserBooks.filter(response='D').count()
            book.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            book.likes = likes
            book.dislikes = dislikes
        return allBooks

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
PUT: userBook relation, uses for response and bookmark
"""
class BookReactionView(generics.GenericAPIView):
    serializer_class = userBookDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, bookId):
        book = get_object_or_404(Book, pk=bookId)
        try:
            tmpUserBook = userBook.objects.get(book=bookId, user=request.user)  # get one
        except userBook.DoesNotExist:
            tmpUserBook = None
        rateScore = int(request.data['rateScore'])  # by default, it's a str
        isRated = True if rateScore > 0 else False
        if tmpUserBook:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserBook, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book, user=request.user, isRated=isRated, updatedAt=timezone.now())
            return Response({"message": "Update userBook Successfully"}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book, user=request.user, isRated=isRated)
            return Response({"message": "Add userBook Successfully"}, status=status.HTTP_201_CREATED)