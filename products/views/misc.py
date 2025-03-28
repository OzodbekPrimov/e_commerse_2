from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from products.models import Category, Review, Order, ProductViewHistory, FlashSale
from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework.permissions import IsAuthenticated
from products.permissions import IsStaffOrReadOnly
from products.serializers import CategorySerializer, ReviewSerializer, OrderSerializer, ProductViewHistorySerializer
from products.filters import FlashSaleFilter, OrderFilter


class CustomPagination(PageNumberPagination):
    page_size = 4


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    pagination_class = CustomPagination
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['name']


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['product__name']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = OrderFilter
    search_fields = ['status']

    permission_classes = [IsStaffOrReadOnly]







