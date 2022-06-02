import operator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from drf_yasg.utils import swagger_auto_schema


from ..serializers.movieSerializers import *
from ..serializers.userRelationsSerializers import UserMovieDetailSerializer
from ..utils import *
from ..models.movies import Movie
from ..models.userRelations import UserMovie


""" For Admin(superuser)
GET: Get Movie Detail By Id  # for any
PUT: Update Movie By Id      # for superuser
DELETE: Delete Movie By Id (set isDelete = True)     # for superuser
"""
class MovieDetailView(generics.GenericAPIView):
    serializer_class = MovieDetailSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return MovieProfileSerializer
        return MovieDetailSerializer

    # Get Movie Detail By Id
    @swagger_auto_schema(operation_summary="Get Movie Detail By Id")
    def get(self, request, movieId):
        try:
            movie = get_object_or_404(Movie, pk=movieId)
            allUserMovies = UserMovie.objects.filter(movie=movie)
            rating = allUserMovies.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserMovies.filter(response='L').count()
            dislikes = allUserMovies.filter(response='D').count()
            # rateScore using aggregate method, will return dic, and name is field__avg, value=null if no result
            movie.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            movie.likes = likes
            movie.dislikes = dislikes
            movie.response = 'O'
            movie.isRate = False
            movie.isSave = False
            movie.score = 0
            if not request.user.is_anonymous:
                usermovie =  UserMovie.objects.filter(user=self.request.user,movie=movie).first()
                if usermovie:
                    if usermovie.response == 'L':
                        movie.response = 'L'
                    if usermovie.response == 'D':
                        movie.response = 'D'
                    if usermovie.isRated:
                        movie.isRate = True
                        movie.score = usermovie.rateScore
                    if usermovie.isSaved:
                        movie.isSave = True
            serializer = self.get_serializer(instance=movie)
            data = serializer.data
            data['message'] = "Get Movie Detail Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Movie Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Movie By Id
    @swagger_auto_schema(operation_summary="Update Movie By Id")
    def put(self, request, movieId):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for update movie"}, status=status.HTTP_401_UNAUTHORIZED)
            movie = get_object_or_404(Movie, pk=movieId)
            serializer = self.get_serializer(instance=movie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update Movie Successfully"
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Update Movie Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Delete Movie By Id
    @swagger_auto_schema(operation_summary="Delete Movie By Id")
    def delete(self, request, movieId):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for delete movie"}, status=status.HTTP_401_UNAUTHORIZED)
            movie = get_object_or_404(Movie, pk=movieId)
            movie.delete()
            return Response({"message": "Delete Movie Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Movie Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
POST: Create Movie
"""
class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="Create Movie By Id")
    def post(self, request):
        try:
            if not request.user.is_staff:
                return Response({"message": "Unauthorized for create movie"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            data['message'] = "Create Movie Successfully"
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "Create Movie Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Movies
"""
class MovieListView(generics.ListAPIView):
    serializer_class = ListMovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Get All Movies
    @swagger_auto_schema(operation_summary="Get All Movies")
    def get_queryset(self):
        orderBy = self.request.GET.get('orderBy')
        search = self.request.GET.get('search')
        searchName = self.request.GET.get('searchName')
        category = self.request.GET.get('category')
        savedBy = self.request.GET.get('savedBy')  #savedBy = userId
        area = self.request.GET.get('area') 

        filter = Q()
        if search is not None:
            searchTerms = search.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term) | Q(director__icontains=term) | Q(actor__icontains=term)
        
        if searchName is not None:
            searchTerms = searchName.split(' ')
            for term in searchTerms:
                filter &= Q(title__icontains=term)
        
        
        if category is not None:
            filter &= Q(category=category)

        if savedBy is not None:
            filter &= Q(usermovie__user=savedBy, usermovie__isSaved = True)
        
        if area is not None:
            filter &= Q(area=area)

        allMovies = Movie.objects.filter(filter).order_by('-createdAt')
        for movie in allMovies:
            allUserMovies = UserMovie.objects.filter(movie=movie)
            rating = allUserMovies.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserMovies.filter(response='L').count()
            dislikes = allUserMovies.filter(response='D').count()
            movie.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            movie.likes = likes
            movie.dislikes = dislikes
            movie.response = 'O'
            movie.isRate = False
            movie.isSave = False
            movie.score = 0
            if not self.request.user.is_anonymous:
                usermovie =  UserMovie.objects.filter(user=self.request.user,movie=movie).first()
                if usermovie:
                    if usermovie.response == 'L':
                        movie.response = 'L'
                    if usermovie.response == 'D':
                        movie.response = 'D'
                    if usermovie.isRated:
                        movie.isRate = True
                        movie.score = usermovie.rateScore
                    if usermovie.isSaved:
                        movie.isSave = True

        if orderBy == 'l':
            orderBy = 'likes'
        elif orderBy == 'd':
            orderBy = 'dislikes'
        elif orderBy == 'r':
            orderBy = 'rating'
        else:
            return allMovies

        ordered = sorted(allMovies, key=operator.attrgetter(orderBy), reverse=True)

        return ordered


"""
PUT: UserMovie relation, uses for response and save
"""
class MovieReactionView(generics.GenericAPIView):
    serializer_class = UserMovieDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="React On Movie, ie. Likes, Dislikes, Rating")
    def put(self, request, movieId):
        request.data._mutable = True
        movie = get_object_or_404(Movie, pk=movieId)
        try:
            tmpUserMovie = UserMovie.objects.get(movie=movieId, user=request.user)  # get one
        except UserMovie.DoesNotExist:
            tmpUserMovie = None

        isRated = False
        rateScore = int(request.data['rateScore'])  # by default, it's a str
        
        if rateScore > 0:
            isRated = True
        else:
            if tmpUserMovie:
                if tmpUserMovie.rateScore > 0:
                    request.data['rateScore'] = tmpUserMovie.rateScore
                    isRated = True
                else:
                    isRated = False
        if tmpUserMovie:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserMovie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie=movie, user=request.user, isRated=isRated, updatedAt=timezone.now())
            data = serializer.data
            data['message'] = "Update UserMovie Successfully"
            return Response(data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie=movie, user=request.user, isRated=isRated)
            data = serializer.data
            data['message'] = "Add UserMovie Successfully"
            return Response(data, status=status.HTTP_201_CREATED)