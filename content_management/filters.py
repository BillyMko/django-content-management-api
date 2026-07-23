import django_filters
from .models import Content

class ContentFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(field_name="category__slug",
                                         lookup_expr="exact")
    
    tag = django_filters.CharFilter(field_name="tags",
                                    lookup_expr="exact")
    
    
    class Meta:
        model = Content

        fields = ["category", "tag", "difficulty"]
