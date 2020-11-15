from main.models import ProductCategory
import django_filters
from django.db.models import Q, Count

# class AdminCategoryFilterSet(django_filters.FilterSet):
#     parent__isnull = django_filters.BooleanFilter(field_name='parent', lookup_expr='isnull')

#     class Meta:
#         models = ProductCategory
#         fields = ['parent__isnull']