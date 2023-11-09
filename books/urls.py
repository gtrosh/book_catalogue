from django.urls import path

from .views import BookDetailView, BookListView, FavouritesViewSet, ReviewView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('reviews/', ReviewView.as_view(), name='review'),
    path('favourites/', FavouritesViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorites'),
]