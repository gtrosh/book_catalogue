import requests
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import BookFilter
from .models import Book, FavouriteBook, Review
from .serializers import (BookListSerializer, BookSerializer,
                          FavouritesSerializer, ReviewSerializer,
                          UserSerializer)


class BookListView(generics.ListAPIView):
    """Список книг"""

    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [IsAuthenticated]


class BookDetailView(generics.RetrieveAPIView):
    """Информация о книге"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class ReviewView(generics.ListCreateAPIView):
    """Отзывы о книгах"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class FavouritesViewSet(viewsets.ViewSet):
    """Избранное"""

    permission_classes = [IsAuthenticated]

    def list(self, request):

        queryset = FavouriteBook.objects.filter(user=request.user)
        serializer = FavouritesSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):

        serializer = FavouritesSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        queryset = Book.objects.all()
        book_id = validated_data.get('book')
        book = get_object_or_404(queryset, title=book_id)
        user = request.user
        
        favourite_book, _ = FavouriteBook.objects.get_or_create(
            user=user, book=book
        )
        serializer = FavouritesSerializer(favourite_book, context={'request': request})
        return Response(serializer.data)


class ActivateUser(generics.GenericAPIView):
    """Активация пользователя"""
    
    serializer_class = UserSerializer
    
    def get(self, request, uid, token, format = None):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/auth/users/activation/"
        response = requests.post(url, data = payload)

        if response.status_code == 204:
            return Response({'message': 'Аккаунт успешно активирован'}, response.status_code)
        else:
            return Response(response.json())
