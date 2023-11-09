import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    publication_date = django_filters.DateFromToRangeFilter(help_text='Введите дату в формате: от YYYY-MM-DD до YYYY-MM-DD')
    
    class Meta:
        model = Book
        fields = {
            'genre', 'author', 'publication_date'
        }
