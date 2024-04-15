from django_filters.filters import CharFilter, DateTimeFilter
from django_filters import FilterSet

from fav_link.models import FavoriteUrl


class FavoriteUrlFilter(FilterSet):

    title = CharFilter(field_name="title", lookup_expr="icontains")
    url = CharFilter(field_name="url", lookup_expr="icontains")

    start_date = DateTimeFilter(field_name="create_at", lookup_expr="date__gte")
    end_date = DateTimeFilter(field_name="create_at", lookup_expr="date__lte")

    category = CharFilter(field_name="category__name", lookup_expr="icontains")

    tags = CharFilter(field_name="tags", method="filter_tags")

    class Meta:
        model = FavoriteUrl
        fields = {}

    def filter_tags(self, queryset, name, value):
        tags = [tag.strip() for tag in value.split(",")]
        return queryset.filter(tags__name__in=tags)
