import django_filters

from yamdb.models import Titles


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre',
        lookup_expr='slug'
    )
    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='slug'
    )
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    year = django_filters.CharFilter(field_name='year', lookup_expr='contains')

    class Meta:
        model = Titles
        fields = ('genre', 'category', 'name', 'year')
