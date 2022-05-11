from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions


from ..serializers.movieSerializers import *
from ..serializers.userRelationsSerializers import userMovieDetailSerializer
from ..utils import *
from ..models.movies import Movie
from ..models.userRelations import userMovie


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
    def get(self, request, movieId):
        try:
            movie = get_object_or_404(Movie, pk=movieId)
            allUserMovies = userMovie.objects.filter(movie=movie)
            rating = allUserMovies.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserMovies.filter(response='L').count()
            dislikes = allUserMovies.filter(response='D').count()
            # rateScore using aggregate method, will return dic, and name is field__avg, value=null if no result
            movie.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            movie.likes = likes
            movie.dislikes = dislikes
            serializer = self.get_serializer(instance=movie)
            return Response(data=serializer.data ,status=status.HTTP_200_OK)
        except:
            return Response({"message": "Get Movie Detail Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Update Movie By Id
    def put(self, request, movieId):
        movie = get_object_or_404(Movie, pk=movieId)
        serializer = self.get_serializer(instance=movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updatedAt=timezone.now())
        return Response({"message": "Update Movie Successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    # Delete Movie By Id
    def delete(self, request, movieId):
        try:
            movie = get_object_or_404(Movie, pk=movieId)
            movie.delete()
            return Response({"message": "Delete Movie Successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Delete Movie Failed"}, status=status.HTTP_400_BAD_REQUEST)


"""
GET: Get All Movies
POST: Create Movie
"""
class MovieListAndCreateView(generics.ListCreateAPIView):
    serializer_class = ListMovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ListMovieSerializer
        return MovieCreateSerializer

    # Get All Movies
    def get_queryset(self):
        allMovies = Movie.objects.filter()
        for movie in allMovies:
            allUserMovies = userMovie.objects.filter(movie=movie)
            rating = allUserMovies.filter(isRated=True).aggregate(Avg('rateScore'))
            likes = allUserMovies.filter(response='L').count()
            dislikes = allUserMovies.filter(response='D').count()
            movie.rating = rating['rateScore__avg'] if rating['rateScore__avg'] else 0
            movie.likes = likes
            movie.dislikes = dislikes
        return allMovies

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
PUT: userMovie relation, uses for response and save
"""
class MovieReactionView(generics.GenericAPIView):
    serializer_class = userMovieDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, movieId):
        movie = get_object_or_404(Movie, pk=movieId)
        try:
            tmpUserMovie = userMovie.objects.get(movie=movieId, user=request.user)  # get one
        except userMovie.DoesNotExist:
            tmpUserMovie = None
        rateScore = int(request.data['rateScore'])  # by default, it's a str
        isRated = True if rateScore > 0 else False
        if tmpUserMovie:
            """
                instance take one, but filter return list, so need to specify index.
                instead, use objects.get to get a single instance
            """
            serializer = self.get_serializer(instance=tmpUserMovie, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie=movie, user=request.user, isRated=isRated, updatedAt=timezone.now())
            return Response({"message": "Update userMovie Successfully"}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie=movie, user=request.user, isRated=isRated)
            return Response({"message": "Add userMovie Successfully"}, status=status.HTTP_201_CREATED)