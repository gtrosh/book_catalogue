from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, F
from rest_framework import serializers

from .models import Book, FavouriteBook, Review


class MyMinValueValidator(MinValueValidator):
    message = "Рейтинг не может быть меньше %(limit_value)s."


class MyMaxValueValidator(MaxValueValidator):
    message = "Рейтинг не может быть больше %(limit_value)s."


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        validators=[MyMinValueValidator(1), MyMaxValueValidator(5)], label='Рейтинг'
    )
    book_name = serializers.CharField(source='book.title', allow_blank=True, required=False)
    user_name = serializers.CharField(source='user.username', allow_blank=True, required=False)
    
    class Meta:
        model = Review
        fields = ['user', 'book', 'rating', 'text', 'book_name', 'user_name']
        read_only_fields = ['user', 'book_name', 'user_name']

    def create(self, validated_data):
        user = self.context['request'].user  
        book = validated_data['book']
        review, _ = Review.objects.update_or_create(user=user, book=book, defaults=validated_data)
        return review

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        fields_to_pop = {
            'GET': ['user', 'book'],
            'POST': ['book_name', 'user_name']
        }
        for field in fields_to_pop.get(request_method, []):
            fields.pop(field)
        return fields


class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(label='Автор')
    genre = serializers.StringRelatedField(label='Жанр')
    is_favourite = serializers.SerializerMethodField(label='В избранном')
    average_rating = serializers.SerializerMethodField(label='Средний рейтинг')
    reviews = serializers.SerializerMethodField(label='Отзывы')
    
    def get_is_favourite(self, object: Book) -> bool:
        request = self.context.get('request', None)
        if request:
            user = request.user
            if object.title in FavouriteBook.objects.filter(user=user).values_list('book__title', flat=True):
                return True
        return False

    def get_average_rating(self, object: Book):
        reviews = Review.objects.filter(book=object)
        avg_rating = 'N/A'
        if reviews:
            avg_rating = round(reviews.aggregate(Avg('rating')).get("rating__avg"), 2)
        return avg_rating
    
    def get_reviews(self, object: Book):
        return Review.objects.filter(book=object).values('rating', 'text', author=F('user__username'))
        
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'publication_date', 'is_favourite', 'average_rating', 'reviews']


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ['url', 'title', 'author', 'genre', 'is_favourite', 'average_rating']


class FavouritesSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', required=False, allow_blank=True)
    class Meta:
        model = FavouriteBook
        fields = ['user', 'book', 'book_title']
        read_only_fields = ['user']

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        if request_method == 'GET':
            fields.pop('user')
        return fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'