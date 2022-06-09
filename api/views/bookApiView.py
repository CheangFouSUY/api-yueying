import operator
from urllib import response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Q
from platformdirs import user_config_dir
from requests import request
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema

from ..serializers.bookSerializers import *
from ..serializers.userRelationsSerializers import UserBookDetailSerializer
from ..models.books import Book
from ..models.userRelations import UserBook
from ..api_throttles import *

""" For Admin(superuser)
GET: Get Book Detail By Id  # for any
PUT: Update Book By Id      # for superuser
DELETE: Delete Book By Id (set isDelete = True)     # for superuser
"""
class BookDetailView(generics.GenericAPIView):
    serializer_class = BookDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BookProfileSerializer
        return BookDetailSerializer

    # Get Book Detail By Id
    @swagger_auto_schema(operation_summary="Get Book Detail By Id")
    def get(self, request, bookId):
        try:
            book = get_object_or_404(Book, pk=bookId)
            allUserBooks = UserBook.objects.filter(book=book)
            rating = allUserBooks.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserBooks.filter(response='L').count()
            dislikes = allUserBooks.filter(response='D').count()
            # rateScore using aggregate method, will return dic, and name is field__avg, value=null if no result
            book.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            book.likes = likes
            book.dislikes = dislikes
            book.response = 'O'
            book.isRate = False
            book.isSave = False
            book.score = 0
            if not request.user.is_anonymous:
                userbook = UserBook.objects.filter(user=self.request.user,book=book).first()
                if userbook:
                    if userbook.response == 'L':
                        book.response = 'L'
                    if userbook.response == 'D':
                        book.response = 'D'
                    if userbook.isRated:
                        book.isRate = True
                        book.score = userbook.rateScore
                    if userbook.isSaved:
                        book.isSave = True
            serializer = self.get_serializer(instance=book)
            data = serializer.data
            data['message'] = "Get Book Detail Successfully"
            print(data)
            return Response(data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Book Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Book By Id
    @swagger_auto_schema(operation_summary="Update Book By Id")
    def put(self, request, bookId):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for update book"}, status=status.HTTP_401_UNAUTHORIZED)
            book = get_object_or_404(Book, pk=bookId)
            serializer = self.get_serializer(instance=book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Book Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Book Failed"}, status=status.HTTP_401_UNAUTHORIZED)

    # Delete Book By Id
    @swagger_auto_schema(operation_summary="Delete Book By Id")
    def delete(self, request, bookId):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for delete book"}, status=status.HTTP_401_UNAUTHORIZED)
            book = get_object_or_404(Book, pk=bookId)
            book.delete()
            return Response({"message": "Delete Book Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Book Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Book
"""
class BookCreateView(generics.CreateAPIView):
    serializer_class = BookCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="Create Book")
    def post(self, request):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for create book"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            data['message'] = "Create Book Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create Book Failed"}, status=status.HTTP_400_BAD_REQUEST)

"""
GET: Get All Books
"""
class BookListView(generics.ListAPIView):
    serializer_class = ListBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    # Get All Books
    @swagger_auto_schema(operation_summary="Get All Books")
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')
        searchName = self.request.GET.get('searchName')
        category = self.request.GET.get('category')
        savedBy = self.request.GET.get('savedBy')  #savedBy = userId
        isSaved = self.request.GET.get('isSaved') or None

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(isbn__icontains=term) | Q(title__icontains=term) | Q(author__icontains=term) | Q(publisher__icontains=term)
        
        if searchName is not None:
            searchTerms = searchName.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term)
        
        if category is not None:
            filter &= Q(category=category)

        if savedBy is not None:
            filter &= Q(userbook__user=savedBy, userbook__isSaved = True)

        if isSaved is not None and isSaved == 'True' and not self.request.user.is_anonymous:
            allBooks = UserBook.objects.filter(user=self.request.user, isSaved=isSaved).order_by('-createdAt')
            books = []
            for b in allBooks:
                books.append(b.book)
            allBooks = books
        else:
            allBooks = Book.objects.filter(filter).order_by('-createdAt')

        for book in allBooks:
            allUserBooks = UserBook.objects.filter(book=book)
            rating = allUserBooks.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserBooks.filter(response='L').count()
            dislikes = allUserBooks.filter(response='D').count()
            book.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            book.likes = likes
            book.dislikes = dislikes
            book.response = 'O'
            book.isRate = False
            book.isSave = False
            book.score = 0
            if not self.request.user.is_anonymous:
                userbook = UserBook.objects.filter(user=self.request.user,book=book).first()
                if userbook:
                    if userbook.response == 'L':
                        book.response = 'L'
                    if userbook.response == 'D':
                        book.response = 'D'
                    if userbook.isRated:
                        book.isRate = True
                        book.score = userbook.rateScore
                    if userbook.isSaved:
                        book.isSave = True

        if orderBy == 'l':
            orderBy = 'likes'
        elif orderBy == 'd':
            orderBy = 'dislikes'
        elif orderBy == 'r':
            orderBy = 'rating'
        else:
            return allBooks

        ordered = sorted(allBooks, key=operator.attrgetter(orderBy), reverse=True)
        return ordered


"""
PUT: UserBook relation, uses for response and bookmark
"""
class BookReactionView(generics.GenericAPIView):
    serializer_class = UserBookDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [anonRelaxed, userRelaxed]

    @swagger_auto_schema(operation_summary="React On Book, ie. Likes, Dislikes, Rating")
    def put(self, request, bookId):
        request.data._mutable = True
        book = get_object_or_404(Book, pk=bookId)
        try:
            tmpUserBook = UserBook.objects.get(book=bookId, user=request.user)  # get one
        except UserBook.DoesNotExist:
            tmpUserBook = None
        isRated = False
        rateScore = int(request.data['rateScore'])  # by default, it's a str
        if rateScore > 0:
            isRated = True
        else:
            if tmpUserBook:
                if tmpUserBook.rateScore > 0:
                    request.data['rateScore'] = tmpUserBook.rateScore
                    isRated = True
                else:
                    isRated = False
        if tmpUserBook:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserBook, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book, user=request.user, isRated=isRated, updatedAt=timezone.now())
            data = serializer.data
            print(data)
            data['message'] = "Update UserBook Successfully"
            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(book=book, user=request.user, isRated=isRated)
            data = serializer.data
            data['message'] = "Add UserBook Successfully"
            print(data)
            return Response(data, status=status.HTTP_201_CREATED)