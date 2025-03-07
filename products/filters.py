

from .models import Product, FlashSale, Order, STATUS_CHOISES
from django_filters import rest_framework as django_filters


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']


class FlashSaleFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(
        field_name='product__name', lookup_expr='icontains'
    )
    min_discount = django_filters.NumberFilter(
        field_name='discount_percentage', lookup_expr='gte'
    )
    max_discount = django_filters.NumberFilter(
        field_name='discount_percentage', lookup_expr='lte'
    )
    start_date = django_filters.DateTimeFilter(
        field_name='start_time', lookup_expr='gte'
    )
    end_date = django_filters.DateTimeFilter(
        field_name='end_time', lookup_expr='lte'
    )

    class Meta:
        model = FlashSale
        fields = ['product_name', 'min_discount', 'max_discount', 'start_date', 'end_date']


class OrderFilter(django_filters.FilterSet):
    order_status = django_filters.ChoiceFilter(field_name='status',choices=STATUS_CHOISES,lookup_expr='iexact', label='Order status')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter('created_at', lookup_expr='lte')
    min_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte', label='Minimum quantity')
    max_quantity = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte', label='Maximum quantity')

    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'status', 'created_at']
