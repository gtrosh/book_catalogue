from django.contrib import admin

from .models import Author, Book, FavouriteBook, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'author', 'publication_date', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'text')

@admin.register(FavouriteBook)
class FavouriteBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')
