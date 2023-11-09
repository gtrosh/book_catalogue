from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя и фамилия автора')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self) -> str:
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    publication_date = models.DateField(verbose_name='Дата публикации')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Текст отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self) -> str:
        return f'{self.text[:50]}{"..."}'
    

class FavouriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')

    class Meta:
        verbose_name = 'Избранная книга'
        verbose_name_plural = 'Избранные книги'

    def __str__(self) -> str:
        return self.book.title
