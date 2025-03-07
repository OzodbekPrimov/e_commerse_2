from django_filters import rest_framework as django_filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from .filters import ProductFilter
from drf_yasg import  openapi
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from  rest_framework import viewsets
from .models import Category, Product, Review
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class CustomPagination(PageNumberPagination):
    page_size = 3


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ProductViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = CustomPagination  # api/products/?page=2

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'min_price', openapi.IN_QUERY, description='Minimum price', type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY, description='Maximum price', type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description='Product category', type=openapi.TYPE_STRING
            ),
        ]
    )


    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_product = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer = ProductSerializer(related_product, many=True)
        return Response({
            'product':serializer.data,
            'related_products':related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        top_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:2]
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        print(reviews)
        if reviews.count()==0:
            return Response({'average_rating':"No reviews yet!"})
        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating":avg_rating})

